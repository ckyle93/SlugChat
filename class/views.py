from django.http import HttpResponseRedirect
from django.shortcuts import render
from slugchat.functions import logged_in


def class_chat(request):
    user = logged_in(request)
    if user is None:
        return HttpResponseRedirect('/')

    context = {'firstname': user.firstName,
                'currentclass': request.GET.get('class', '')}
    return render(request, 'class/class_chat.html', context)

def give_quiz(request):
    user = logged_in(request)

    if user is None:
        return HttpResponseRedirect('/')

    status = user.get_status();
    if request.method == 'POST':
            # If user hit Delete button, delete from db only if the user is
            # enrolled in this class.
            if request.POST.get('delete', '') is not '':
                user.roster_set.get(courseID=course).delete()
            # Else if the user isn't already enrolled in this course
            # enroll them.
            elif (request.POST.get('delete', '') is '' and
                  not user.roster_set.all().filter(courseID=course).exists()):
                roster_form.save()
            return HttpResponseRedirect('/profile/')
    else:
        roster_form = RosterForm()




