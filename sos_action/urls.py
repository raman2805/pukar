from django.conf.urls import patterns, url
from sos_action import views
urlpatterns = patterns('', 
                       url(r'^$', views.index, name='index'),
                       url(r'add_action/([0-9]+)$', views.add_action, name = 'add_action'),
                       url(r'add_action/', views.add_action, name = 'add_action'),
                       url(r'complaint/([0-9]*)', views.view_complaint, name = 'view_complaint'),
                       url(r'list_actions/', views.list_actions, name = 'list_actions'),
                       url(r'list_complaints/', views.list_complaints, name = 'list_complaints')
                      )

