from django.contrib import admin

from .models import FileDB, Comment

admin.site.register(FileDB)
admin.site.register(Comment)
