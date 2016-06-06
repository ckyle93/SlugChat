from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^check_answer/', views.check_answer, name='check_answer'),
    url(r'^pick_quiz/', views.pick_quiz, name='pick_quiz'),
    url(r'^quiz/', views.quiz_choices, name='quiz_choices'),
    url(r'^$', views.class_chat, name='class_chat'),
]
