from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from home.models import User, Roster, Course, Quiz, QuizChoices
from userpage.forms import UserForm, RosterForm, CourseForm, QuizForm
from userpage.forms import QuizChoicesForm

from slugchat.functions import logged_in, QuizObj


# This is the function that takes the info from google sign in, then adds the
# user to the database if they are not already in the database. The
# request.session key 'email_address' is also set in this function, which is
# the backbone of the login system.
@csrf_exempt
def tokensignin(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email_address = request.POST['email_address']
    profile_pic = request.POST['profile_pic']

    # Set the request.ssession variable. This keeps track of the user's
    # logged in state.
    request.session['email_address'] = email_address

    # New user who has never signed in before, save their data to the database.
    if(not User.objects.filter(email=email_address).exists()):
        user_info = User(firstName=first_name, lastName=last_name,
                         email=email_address, profile_pic=profile_pic)
        user_info.save()
    else:
        user_info = User.objects.get(email=email_address)

    classes = user_info.roster_set.all().all()
    return render(request, 'home/ajax_class_request.html',
                  {'classes': classes})


def signout(request):
    if logged_in(request):
        del request.session['email_address']
    return HttpResponseRedirect('/')


# Displays the profile information for the user.
def profile(request):

    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']
    instance = User.objects.get(email=email_address)

    # Redirect user to build profile page if they haven't completed
    # their profile
    if instance.completeProfile is False:
        return HttpResponseRedirect('/profile/buildprofile/')
    # Here we grab all the courses that the current user has enrolled in
    rosters = instance.roster_set.all()

    try:
        with open('key_file.txt', 'r') as f:
            GOOGLE_KEY = f.read().rstrip()
    except IOError:
        GOOGLE_KEY = None
        print("key_file not found. \nMessage Ckyle for key_file.txt")

    context = {'full_name': instance.firstName + " " + instance.lastName,
               'school': instance.school,
               'studentID': instance.studentID,
               'email': instance.email,
               'status': instance.get_status(),
               'profile_pic': instance.profile_pic,
               'classes': rosters.all(),
               'GOOGLE_KEY': GOOGLE_KEY}

    return render(request, 'userpage/profile.html', context)


# This page allows a user to update fields in their user profile.
# Interactions with the db are done using model forms, which take
# care of building the forms to display.
#
# The user comes to this page in one of two ways. First, when they fist log
# in to our app, they will be directed here to complete their profile. Second,
# they can go to /buildprofile/?update=true and they will be able to update
# their profile again.
#
# user_form is sent to the template, it contains the fields:
#   firstName, lastName, profile_pic, school, studentID, and status.
def buildprofile(request):

    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    # If this user's profile is complete, and they aren't coming here to
    # update their profile, redirect to profile page
    if (not request.GET.get('update', '') == 'true' and
            User.objects.filter(
            email=email_address, completeProfile=True).exists()):
        return HttpResponseRedirect('/profile/')

    # We get the current user and assign it to the user variable, then
    # tell the model form that we want to update the information for
    # this user.
    user = User.objects.get(email=email_address)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user.completeProfile = True
            user_form.save()
            return HttpResponseRedirect('/profile/')
    else:
        user_form = UserForm(instance=user)
    return render(request, 'userpage/buildprofile.html',
                  {'user_form': user_form})


# Only professors can add a class.
def addclass(request):

    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    user = User.objects.get(email=email_address)
    if user.get_status() is not 'Professor':
        return HttpResponse(
                'Sorry, only professors can add classes.', status=401)

    # Create a new course with the current user as the professor
    course = Course(professor=user)
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course_form.save()
            Roster(studentID=user, courseID=course).save()
            return HttpResponseRedirect('/profile/')

    else:
        course_form = CourseForm()

    return render(request, 'userpage/addclass.html',
                  {'course_form': course_form})


# Only professors can delete a class.
def deleteclass(request):

    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    user = User.objects.get(email=email_address)
    if user.get_status() is not 'Professor':
        return HttpResponse(
                'Sorry, only professors can add classes.', status=401)

    roster = Roster(studentID=user)
    if request.method == 'POST':
        roster_form = RosterForm(request.POST, instance=roster)
        if roster_form.is_valid():
            course = roster_form.cleaned_data['courseID']
            # If user hit Delete button, delete from db if the user is actually
            # enrolled in this class.
            Course.objects.get(title=course).delete()
            return HttpResponseRedirect('/profile/')
    else:
        roster_form = RosterForm()

    return render(request, 'userpage/deleteclass.html',
                  {'roster_form': roster_form})


# Anyone can enroll in a course.
def manage_classes(request):

    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    user = User.objects.get(email=email_address)

    roster = Roster(studentID=user)
    if request.method == 'POST':
        roster_form = RosterForm(request.POST, instance=roster)
        if roster_form.is_valid():
            course = roster_form.cleaned_data['courseID']
            # If user hit Delete button, delete from db if the user is actually
            # enrolled in this class.
            if request.POST.get('delete') and user.roster_set.all().filter(
                    courseID=course).exists():
                print('TEST')
                user.roster_set.get(courseID=course).delete()
            # Else if the user isn't already enrolled in this course
            # enroll them.
            elif not user.roster_set.all().filter(courseID=course).exists():
                roster_form.save()
            return HttpResponseRedirect('/profile/')
    else:
        roster_form = RosterForm()

    return render(request, 'userpage/enroll.html',
                  {'roster_form': roster_form})


def viewquizzes(request):
    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    user = User.objects.get(email=email_address)
    if user.get_status() is not 'Professor':
        return HttpResponse(
                'Sorry, only professors can view.', status=401)

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
    if request.method == 'POST':
        quiz_id = request.POST['id']
        Quiz.objects.get(id=quiz_id).delete()
        return HttpResponseRedirect('/profile/viewquizzes')
    else:
        return render(request, 'userpage/viewquizzes.html',
                      {'quiz_list': quiz_list})


def makequizzes(request):
    if not logged_in(request):
        return HttpResponseRedirect('/')

    email_address = request.session['email_address']

    user = User.objects.get(email=email_address)
    if user.get_status() is not 'Professor':
        return HttpResponse(
                'Sorry, only professors can view.', status=401)

    # If the we are updating a quizz's choices, the urls is
    # /profile/makequizzes/?quiz_id=pk, where pk is the primary key
    # of the Quiz object we want to add choices to.
    key = request.GET.get('quiz_id', '')
    if key is not '':
        quiz = get_object_or_404(Quiz, pk=key)
        new_choice = QuizChoices(quiz=quiz)
        previous_choices = quiz.quizchoices_set.all().all()
        if request.method == 'POST':
            quizchoices_form = QuizChoicesForm(
                    request.POST, instance=new_choice)
            if quizchoices_form.is_valid():
                quizchoices_form.save()
            return HttpResponseRedirect(
                    '/profile/makequizzes/?quiz_id=' + str(quiz.id))
        else:
            quizchoices_form = QuizChoicesForm()

        return render(request, 'userpage/addchoices.html',
                      {'quizchoices_form': quizchoices_form,
                       'previous_choices': previous_choices})

    quiz = Quiz(professor=user)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        if quiz_form.is_valid():
            quiz_form.save()
        return HttpResponseRedirect('/profile/makequizzes/?quiz_id=' +
                                    str(quiz.id))
    else:
        quiz_form = QuizForm()

    return render(request, 'userpage/makequizzes.html',
                  {'quiz_form': quiz_form})
