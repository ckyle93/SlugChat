from django.db import models
from home.models import Course
from home.models import User
from datetime import datetime
# 
# Create your models here.
file_dir = './static/uploads/'

class FileDB(models.Model):
	fileObj = models.FileField(upload_to=file_dir)
	fileName = models.CharField(max_length = 20)
	className = models.CharField(max_length = 20, default='')

#the real Comment table. must change referenced table.
class Comment(models.Model):
    #change the following line to reference whatever table is desired
    file = models.ForeignKey(FileDB, on_delete=models.CASCADE)
    
    #the comment itself, simple text field
    comment = models.CharField(max_length=200)
    
    #creates a reference to the user who made the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #pub_date is auto pulled. make sure datetime import is present
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.comment
