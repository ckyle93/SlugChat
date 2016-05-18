from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^buildprofile/', views.buildprofile, name='buildprofile'),
    url(r'^tokensignin/', views.tokensignin, name='tokensignin'),
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^testprofile/$', views.testprofile, name='testprofile'),
]
