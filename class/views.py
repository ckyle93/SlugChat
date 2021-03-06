from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render
from slugchat.functions import logged_in, QuizObj
# from home.models import Course
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

    context = {'firstname': user.firstName, 'status': status,
               'quiz_list': quiz_list}

    #return render(request, 'class/quiz_test.html', context)
    #return render(request, 'class/mainAppPageStudent.html', context)
    return render(request, 'class/mainAppPageInstructor.html', context)


@csrf_exempt
def pick_quiz(request):
    quizID = request.POST['quizID']

    quiz = Quiz.objects.get(id=quizID)

    new_quiz = QuizObj()
    new_quiz.question_text = quiz.question
    new_quiz.id = quiz.id
    choices = quiz.quizchoices_set.all().all()
    for choice in choices:
        new_quiz.choices.append(choice)
    context = {'quiz': new_quiz}
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

    currentclass = request.get.get('class', '')

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
