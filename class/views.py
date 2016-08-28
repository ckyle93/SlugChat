from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from slugchat.functions import logged_in, QuizObj
from home.models import Course
from home.models import Quiz


def class_chat(request):
    #  user = logged_in(request)
    #  if user is None:
    #      return HttpResponseRedirect('/')

    #  context = {'firstname': user.firstName,
    #             'currentclass': request.GET.get('class', '')}
    #  return render(request, 'class/class_chat.html', context)
    user = logged_in(request)
    if user is None:
        return HttpResponseRedirect('/')

    currentclass = request.GET.get('class', '')

    if currentclass == '':
        return HttpResponseRedirect('/')

    status = user.get_status()
    if status == 'Professor':
        quizzes = user.quiz_set.all().all()

    context = {'firstname': user.firstName, 'status': status,
               'quiz_list': quizzes}
    return render(request, 'class/quiz_test.html', context)


@csrf_exempt
def pick_quiz(request):
    quizID = request.POST['quizID']
    # className = request.POST['class']

    quiz = Quiz.objects.get(id=quizID)
    # We may not actually need the class name. TBD
    # Also it doesn't seem to work correctly right now.
    # course = Course.objects.get(title=className)
    context = {'quiz': quiz}

    return render(request, 'class/show_quiz.html', context)


@csrf_exempt
def check_answer(request):
    quizID = request.POST['quizID']
    choiceID = request.POST['choice']

    quiz = Quiz.objects.get(id=quizID)

    if quiz.quizchoices_set.filter(id=choiceID, correct=True).exists():
        return render(request, 'class/correct.html')
    else:
        return render(request, 'class/incorrect.html')


def quiz_choices(request):
    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    currentclass = request.GET.get('class', '')

    if currentclass == '':
        return HttpResponseRedirect('/')

    status = user.get_status()
    if status == 'professor':
        quizzes = user.quiz_set.all().all()
        quiz_list = []
        for quiz in quizzes:
            new_quiz = QuizObj()
            new_quiz.question_text = quiz.question
            new_quiz.id = quiz.id
            choices = quiz.quizchoices_set.all().all()
            for choice in choices:
                new_quiz.choices.append(choice.choice)
            quiz_list.append(new_quiz)
    else:
        quiz_list = []

    context = {'firstname': user.firstname, 'status': status,
               'quiz_list': quiz_list}
    return render(request, 'class/quiz_test.html', context)


@csrf_exempt
def check_quiz(request):
    return HttpResponse("hello", 400)
#     user = logged_in(request)
# 
#     if user is None:
#         return HttpResponseRedirect('/')
# 
#     # currentclass = request.GET.get('class', '')
# 
#     if currentclass == '':
#         return HttpResponseRedirect('/')
# 
#     if not Course.objects.filter(title=currentclass).exists():
#         return HttpResponseRedirect('/')
# 
#     if not Course.objects.get(title=currentclass, activeQuiz=True):
#         return HttpResponse('')
# 
#     course = Course.objects.get(title=currentclass)
#     quizID = course.quizID
# 
#     quiz = Quiz.objects.get(id=quizID)
# 
#     new_quiz = QuizObj()
#     new_quiz.question_text = quiz.question
#     new_quiz.id = quiz.id
#     choices = quiz.quizchoices_set.all().all()
#     for choice in choices:
#         new_quiz.choices.append(choice)
#     context = {'quiz': new_quiz}
#     return render(request, 'class/show_quiz.html', context)



# def give_quiz(request):
#    user = logged_in(request)
#
#    if user is None:
#        return HttpResponseRedirect('/')
#
#    course_title = request.POST['title']
#
#    # Check if there is a quiz being given
#    if Course.objects.filter(title=course_title, activeQuiz=True).exists():
#        return render(request, 'class/ajax_quiz.html', context)
#    status = user.get_status();
#
#    context = {'firstname': user.firstName,
#                'currentclass': request.GET.get('class', '')}
#    #return render(request, 'class/class_chat.html', context)
#    return render(request, 'class/mainAppPage.html', context)
