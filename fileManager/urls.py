from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.generate, name='class_page'),
]
