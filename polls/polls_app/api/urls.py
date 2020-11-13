from polls_app.api import views
from django.urls import path

questions_list = views.QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
question_detail = views.QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

polls_list = views.PollViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
poll_detail = views.PollViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

users_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('users/', users_list),
    path('users/<int:pk>', user_detail),
    path('polls/', polls_list),
    path('polls/<int:pk>', poll_detail),
    path('questions/', questions_list),
    path('questions/<int:pk>', question_detail),
    path('polls/active/', views.ActivePollList.as_view()),
    path('polls/answer/', views.AnswerPoll.as_view()),
]
