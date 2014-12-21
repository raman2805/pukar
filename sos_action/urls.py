from django.conf.urls import patterns, url
from sos_action import views
urlpatterns = patterns('', 
                       url(r'^$', views.index, name='index'),
                       url(r'^complaint/new/', views.AddComplaint, name = 'add_complaint'),
                       url(r'^complaint/([0-9]*)', views.ViewComplaint, name = 'view_complaint'),
                       url(r'^update/([0-9]*)', views.Update, name = 'update'),
                       url(r'^update_info/([0-9]*)', views.UpdateInfo, name = 'update_info'),
                       url(r'^assign_station/([0-9]*)', views.AssignStation, name = 'assign_station'),
                       url(r'^list_complaints/', views.ListComplaints, name = 'list_complaints'),
                       url(r'^register/$', views.Register, name='register'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'sos_action/login.html'}),
                       url(r'^logout/$', views.UserLogout, name='logout')
                      )

