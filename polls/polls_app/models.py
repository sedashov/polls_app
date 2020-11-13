from django.db import models
from polls_app.choices import QUESTION_TYPES, TEXT_ANSWER
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_created=True)
    finish_date = models.DateTimeField()
    description = models.TextField()


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE, blank=True, null=True)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES,
        default=TEXT_ANSWER,
    )
    answer_choices = models.TextField(default='', null=True, blank=True)  # json representation of an array
    answers = models.ManyToManyField(User, through='UserQuestion')


class UserQuestion(models.Model):
    # transitional model between user and question to store answers
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # null and blank for anonymous answers
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()  # json representation of dict of answers
