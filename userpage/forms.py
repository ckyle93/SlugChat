# See https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/
from django.forms import ModelForm

from home.models import User
from home.models import Roster
from home.models import Course
from home.models import Quiz
from home.models import QuizChoices


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'profile_pic',
                  'school', 'studentID', 'status']


class RosterForm(ModelForm):

    class Meta:
        model = Roster
        fields = ['courseID']


class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['ta', 'school', 'title', 'description', 'textbook', 'time']

class QuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = ['question', 'courseID']


class QuizChoicesForm(ModelForm):

    class Meta:
        model = QuizChoices
        exclude = ['quiz']
