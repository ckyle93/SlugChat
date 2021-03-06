from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from home.models import User, Roster, Course, Quiz, QuizChoices
from userpage.forms import UserForm, RosterForm, CourseForm, QuizForm
from userpage.forms import QuizChoicesForm

from slugchat.functions import logged_in, QuizObj, verify_user


# This is the function that takes the info from google sign in, then adds the
# user to the database if they are not already in the database. The
# request.session key 'user' is also set in this function, which is
# the backbone of the login system.
#
# Get an id_token sent through Ajax, verify it by calling verify_user, which is
# defined in slugchat/functions.py. Verify user makes sure this is a real login
# and returns a dictionary with all the values google gives us. Parse them,
# check if this user is not in our database, if so, insert them and redirect to
# /profile/buildprofile/
@csrf_exempt
def tokensignin(request):
    id_token = request.POST['id_token']

    user_info = verify_user(id_token)

    # Login Failed
    if 'error' in user_info:
        return HttpResponse(user_info['error'], status=403)

    # Get google's information on the user
    first_name = user_info.get('given_name', 'No name given')
    last_name = user_info.get('family_name', 'No name given')
    email_address = user_info.get('email', '')
    profile_pic = user_info.get('picture', '')

    # This is our primary key on users
    user_id = user_info['sub']

    # Sub is a unique id for each google user
    request.session['user'] = user_id

    # New user who has never signed in before, save their data to the database.
    if(not User.objects.filter(userID=user_id).exists()):
        user = User(userID=user_id,
                    firstName=first_name, lastName=last_name,
                    email=email_address, profile_pic=profile_pic)
        user.save()
    else:
        user = User.objects.get(userID=user_id)

    classes = user.roster_set.all().all()

    # if the user is not enrolled in any classes, direct them
    # to complete their profile
    if not classes:
        return render(request, 'home/ajax_new_user.html')

    # Otherwise, display a list of links to all of their class pages
    return render(request, 'home/ajax_class_request.html',
                  {'classes': classes})


# If user clicks sign out, sign them out of google and remove their
# 'user' key from our request.session dictionary
def signout(request):
    user = logged_in(request)
    if user is not None:
        del request.session['user']
    return HttpResponseRedirect('/')


# Displays the profile information for the user.
def profile(request):

    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    # Redirect user to build profile page if they haven't completed
    # their profile
    if user.completeProfile is False:
        return HttpResponseRedirect('/profile/buildprofile/')
    # Here we grab all the courses that the current user has enrolled in
    rosters = user.roster_set.all()

    try:
        with open('key_file.txt', 'r') as f:
            GOOGLE_KEY = f.read().rstrip()
    except IOError:
        GOOGLE_KEY = None
        print("key_file not found. \nMessage Ckyle for key_file.txt")

    context = {'full_name': user.firstName + " " + user.lastName,
               'school': user.school,
               'studentID': user.studentID,
               'email': user.email,
               'status': user.get_status(),
               'profile_pic': user.profile_pic,
               'classes': rosters.all(),
               'GOOGLE_KEY': GOOGLE_KEY}

    #return render(request, 'userpage/profile.html', context)
    return render(request, 'userpage/viewMyProfile.html', context)


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

    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    # If this user's profile is complete, and they aren't coming here to
    # update their profile, redirect to profile page
    if (not request.GET.get('update', '') == 'true' and
            user.completeProfile is True):
        return HttpResponseRedirect('/profile/')

    # We get the current user and assign it to the user variable, then
    # tell the model form that we want to update the information for
    # this user.
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user.completeProfile = True
            user_form.save()
            return HttpResponseRedirect('/profile/')
    else:
        user_form = UserForm(instance=user)

    context = {'full_name': user.firstName + " " + user.lastName,
               'school': user.school,
               'studentID': user.studentID,
               'email': user.email,
               'profile_pic': user.profile_pic,
               'user_form': user_form,
               'status': user.get_status()
               }
    #return render(request, 'userpage/buildprofile.html', {'user_form': user_form})
    return render(request, 'userpage/editprofile.html', context)



# Only professors can add a class.
# This creates a new class object
def addclass(request):

    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    if user.get_status() != 'Professor':
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

    status = user.get_status()
    return render(request, 'userpage/addclass.html',
            {'status': status, 'course_form': course_form})


# Only professors can delete a class.
def deleteclass(request):

    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    #if user.get_status() is not 'Professor':
    #    return HttpResponse(
    #            'Sorry, only professors can add classes.', status=401)
    if user.get_status() != 'Professor':
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

    status = user.get_status()
    return render(request, 'userpage/deleteclass.html',
            {'status': status, 'roster_form': roster_form})


# Anyone can enroll in a course.
# Users can enroll and drop classes via this page
def manage_classes(request):

    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    roster = Roster(studentID=user)
    if request.method == 'POST':
        roster_form = RosterForm(request.POST, instance=roster)
        if roster_form.is_valid():
            course = roster_form.cleaned_data['courseID']
            # If user hit Delete button, delete from db only if the user is
            # enrolled in this class.
            if request.POST.get('delete', '') and user.roster_set.all().filter(
                    courseID=course).exists():
                user.roster_set.get(courseID=course).delete()
            # Else if the user isn't already enrolled in this course
            # enroll them.
            elif (request.POST.get('delete', '') is '' and
                  not user.roster_set.all().filter(courseID=course).exists()):
                roster_form.save()
            return HttpResponseRedirect('/profile/')
    else:
        roster_form = RosterForm()

    status = user.get_status()
    return render(request, 'userpage/enroll.html',
                {'status': status, 'roster_form': roster_form})



def viewquizzes(request):
    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

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
    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

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
