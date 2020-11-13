from rest_framework import serializers
from polls_app.models import Poll, Question, UserQuestion
from django.contrib.auth.models import User
import json
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    """
    Django's User Model serializer
    """

    class Meta:
        model = User
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answer_choices = serializers.ListField(child=serializers.CharField(), allow_null=True, default=None)

    def validate(self, data):
        q_type = data.get('question_type', 'T')
        if q_type != 'T' and not data.get('answer_choices'):
            raise serializers.ValidationError('Provide answer choices or change question type')
        ans = data.get('answer_choices', '')
        data['answer_choices'] = json.dumps({'answer_choices': ans})
        return data

    def to_representation(self, instance):
        representation = super(QuestionSerializer, self).to_representation(instance)
        representation['answer_choices'] = json.loads(instance.answer_choices)['answer_choices']
        return representation

    class Meta:
        model = Question
        fields = ['pk', 'question_text', 'question_type', 'answer_choices']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    start_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        q = validated_data.pop('questions', [])
        validated_data['start_date'] = validated_data.pop('start_date', datetime.today())  # if no start date then put today
        poll = Poll.objects.create(**validated_data)
        for question in q:
            obj = Question.objects.create(poll=poll, **question)
            obj.save()
        return poll

    def update(self, instance, validated_data):
        start_date = validated_data.pop('start_date', 0)
        if start_date != 0:
            raise serializers.ValidationError('You can not change start date')
        q = validated_data.pop('questions', instance.questions)
        instance = super(PollSerializer, self).update(instance, validated_data)
        instance.questions.clear()
        for question in q:
            obj = Question.objects.create(poll=instance, **question)
            obj.save()
        return instance

    class Meta:
        model = Poll
        fields = ['pk', 'questions', 'title', 'start_date', 'finish_date', 'description']
        related_object = 'question'
