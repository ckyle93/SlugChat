from django import forms
from django.forms import ModelForm
from fileManager.models import FileDB, Comment

class FileForm(ModelForm):
	class Meta:
		model = FileDB
		fields = ['fileObj', 'fileName', 'className']
		widgets = {'className': forms.HiddenInput()}
		labels = {
            'fileObj': ('File'),
            'fileName': ('Name')
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
