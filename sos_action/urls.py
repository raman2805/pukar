from django.conf.urls import patterns, url
from sos_action import views
urlpatterns = patterns('', url(r'^$', views.index, name='index'))

