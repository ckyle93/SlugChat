import os
from fileManager.models import FileDB
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import FileForm, CommentForm
from .models import file_dir, FileDB, Comment
from home.models import Course
from slugchat.functions import logged_in
from slugchat.settings import MEDIA_ROOT, MEDIA_URL

from datetime import datetime

def upload_file(request, className):
	if request.method == 'POST' and 'fileName' in request.POST:
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			form = FileForm(initial={'className':className})
	else:
		form = FileForm(initial={'className':className})
	return {'dl_form': form}

def download_file(request, className, user):
	files_to_serve = FileDB.objects.filter(className=className)
	print(files_to_serve)
	files = [(MEDIA_URL + x.fileObj.name, x.fileName, x, make_comment(request, user, x)) for x in files_to_serve]
	return {'filelist': files}

def get_course_context(className):
	if className:
		course = Course.objects.filter(title=className)
		course = course[0] # get the one/only object out of result set
		return {'textbook':course.textbook, 'time':course.time, 'description':course.description, 'professor': course.professor}
	else:
		return {}

def make_comment(request, user, file):
	if request.method == 'POST' and 'comment' in request.POST:
		form_to_submit = request.POST.get('file_name','')
		form = CommentForm(request.POST)
		if file.fileName == form_to_submit and form.is_valid():
			comment = form.save(commit=False)
			comment.file = file
			comment.user = user
			comment.pub_date = datetime.now()
			comment.save()
			form = CommentForm()
	else:
		form = CommentForm()
	return form


def generate(request):
	user = logged_in(request)
	if user:
		className = request.GET.get('class', '')
		context = {'status': user.get_status(), 'currentclass':className, 'firstname':user.firstName}
		if user.get_status() == 'Professor':
			context.update(upload_file(request, className))
		context.update(download_file(request, className, user))
		context.update(get_course_context(className))
		return render(request, 'myClassPage.html', context)
	else:
		return HttpResponseRedirect('/')
