from polls_app.models import Question, Poll, UserQuestion
from django.contrib.auth.models import User
from polls_app.api.serializers import (UserSerializer, PollSerializer, QuestionSerializer)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from datetime import datetime
from rest_framework.permissions import IsAdminUser
import json


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PollViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ActivePollList(generics.ListCreateAPIView):
    queryset = Poll.objects.filter(finish_date__gte=datetime.today(), start_date__lte=datetime.today())
    serializer_class = PollSerializer


class QuestionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerPoll(APIView):
    def post(self, request):
        # get user and poll, make sure everything is correct
        answers = request.data.get('answers')  # dict {str(question_id): answer}
        user_id = request.data.get('user_id')
        user_queryset = User.objects.filter(pk=user_id)
        if not len(user_queryset):
            # anonymous user
            user = None
        else:
            user = user_queryset[0]
        poll = request.data.get('poll_id')  # id of a poll
        poll = Poll.objects.filter(pk=poll)
        if len(poll) == 0:
            return Response({"message": "Poll with such id does not exist"}, status=404)
        poll = poll[0]
        if user and len(UserQuestion.objects.filter(user=user, question=poll.questions.all()[0])):
            return Response({"message": "This user has already answered this poll"})

        for question in poll.questions.all():
            # make sure that answered
            if str(question.pk) not in answers.keys():
                return Response({"message": "Not all questions are answered"}, status=400)

            # if answered make sure that answers are from suggested
            if question.question_type == '1V' and answers[str(question.pk)] not in json.loads(question.answer_choices)['answer_choices']:
                return Response({"message": f"Choose one answer to question {question.question_text}"
                    f" from {json.loads(question.answer_choices)}"}, status=400)
            if question.question_type == 'MV':
                if type(answers[str(question.pk)]) is not list:
                    return Response({"message": "Please provide answers in a format of a list"})
                for ans in answers[str(question.pk)]:
                    if ans not in json.loads(question.answer_choices)['answer_choices']:
                        return Response({"message": f"Choose answer to question {question.question_text}"
                            f" from {json.loads(question.answer_choices)}"}, status=400)


        # first check whether all questions are answered correctly, then put answers
        for question in poll.questions.all():
            if question.question_type == '1V' and answers[str(question.pk)] not in json.loads(question.answer_choices)['answer_choices']:
                return Response({"message": "Choose answer "}, status=400)
            if question.question_type != 'MV':
                ans = UserQuestion.objects.create(
                    user=user,
                    question=question,
                    answer=answers[str(question.pk)]
                )
            else:
                ans = UserQuestion.objects.create(
                    user=user,
                    question=question,
                    answer=json.dumps({'answer': answers[str(question.pk)]})
                )
        return Response({"message": "Successfully answered questions"}, status=200)


    def get(self, request):
        """ show answers to questions of a specified user """
        # get user and poll
        user_id = request.data.get('user_id')
        user_queryset = User.objects.filter(pk=user_id)
        if not len(user_queryset):
            # anonymous user
            user = None
            return Response({"message": "Provide correct user_id"}, status=400)
        else:
            user = user_queryset[0]
        poll = request.data.get('poll')
        if poll:
            q = Poll.objects.filter(pk=poll)
        else:
            q = Poll.objects.all()

        # iterate over queryset of polls and write down answers
        polls = dict()
        for poll in q:
            answers = dict()
            for question in poll.questions.all():
                answer = UserQuestion.objects.filter(user=user, question=question)
                if len(answer) == 0 and len(q) == 1:
                    # single-poll query, poll not answered
                    return Response({"message": "This poll has not been answered by this user"}, status=400)
                elif len(answer) != 0:
                    answer = answer[0]
                    if question.question_type != 'MV':
                        answers.update({question.question_text: answer.answer})
                    else:
                        answers.update({question.question_text: json.loads(answer.answer)['answer']})
            if answers:
                polls.update({poll.title: answers})
        return Response(polls, status=200)


