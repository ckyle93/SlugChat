from django import forms
from django.forms import ModelForm
from fileManager.models import FileDB
from fileManager.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class FileForm(ModelForm):
	class Meta:
		model = FileDB
		fields = ['fileObj', 'fileName', 'className']
		widgets = {'className': forms.HiddenInput()}
