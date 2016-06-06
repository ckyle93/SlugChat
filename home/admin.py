from django.contrib import admin

from .models import User, Course, Roster, Quiz, QuizChoices, Grade

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Roster)
admin.site.register(Quiz)
admin.site.register(QuizChoices)
admin.site.register(Grade)
