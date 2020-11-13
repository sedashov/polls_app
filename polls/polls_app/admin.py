from django.contrib import admin
from polls_app.models import Question, Poll, UserQuestion

admin.site.register(Question)
admin.site.register(Poll)
admin.site.register(UserQuestion)
