# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import *
import models
from models import mobappuser, Station, Complaint, Updates
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import sos_action
import datetime
gRanges = list(set([x.range for x in Station.objects.all()]))
gComplaintTypesList = [x[0] for x in sos_action.models.gComplaintTypes]
def index(request) :
  context = RequestContext(request)
  return render_to_response('sos_action/index.html', {}, context)

def AddUpdateToDb(user, complaint, information) :
  update = Updates()
  update.user = user
  update.complaint = complaint
  update.information = information
  update.save()

def AddComplaint(request) : 
  context = RequestContext(request)
  c = Complaint()
  # <to-do-some-sanity-checking>
  if request.method == 'GET' :
    c = Complaint()
    # figure out the userid
    c.complainant = mobappuser.objects.get(id = request.GET.get('mobappuser_id'))
    c.location = request.GET.get('location', 'unknown')
    c.complaint_time = datetime.datetime.now()
    c.status = 'OPEN'
    if request.GET.get('informer', '') != '' :
      c.informer = request.GET.get('informer')
    c.save()
  elif request.method == 'POST' :
    c = Complaint()
    c.location = request.POST.get('location')
    if request.POST.get('informer', '') != '' :
      c.informer = request.POST.get('informer')
    c.status = 'OPEN'
    c.complainant = mobappuser.objects.get(id = request.POST.get('mobappuser_id'))

  return HttpResponseRedirect('/sos_action/update/%s' % (c.id))

@login_required(login_url = '/sos_action/login')
def Update(request, complaint_id) :
  complaint = Complaint.objects.get(id = complaint_id)
  if not complaint.station :
    return HttpResponseRedirect('/sos_action/assign_station/%s' % (complaint_id))
  else :
    return HttpResponseRedirect('/sos_action/update_info/%s' % (complaint_id))

@login_required(login_url = '/sos_login/login')
def UpdateInfo(request, complaint_id) : 
  from sos_action.models import Station, Complaint
  context_dict = {}
  complaint = Complaint.objects.get(id = complaint_id)
  if request.method == 'POST' :
    update_info = request.POST.get('info')
    old_status = complaint.status
    status = request.POST.get('status')
    if status == 'CLOSED' and status != old_status :
      complaint.resolved_time = datetime.datetime.now()
    complaint.status = status
    complaint.save()
    AddUpdateToDb(request.user, complaint, update_info)
    return HttpResponseRedirect('/sos_action/complaint/%s' % complaint_id)
  else :
    context_dict['complaint'] =  complaint
    return render_to_response('sos_action/update_info.html', 
                              context_dict, 
                              RequestContext(request))
 

@login_required(login_url = '/sos_action/login')
def AssignStation(request, complaint_id) :
  from sos_action.models import Station, Complaint
  districts = []
  stations = []
  context = RequestContext(request)
  context_dict = {}
  context_dict['complaint'] = Complaint.objects.get(id = complaint_id)
  context_dict['complaint_types'] = gComplaintTypesList
  if request.method == 'GET' :
    context_dict['selected_complaint_type'] = request.GET.get('complaint_type', '')
    range = request.GET.get('range', '')
    district = request.GET.get('district', '')
    if range != '' :
      context_dict['selected_range'] = range
      districts = list(set([x.district for x in Station.objects.filter(range = range)]))
    if district != '' :
      context_dict['selected_district'] = district
      stations = Station.objects.filter(range = range, district = district)
      
    context_dict['ranges'] = gRanges
    context_dict['districts'] = districts
    context_dict['stations'] = stations
    return render_to_response('sos_action/assign.html', 
                              context_dict, 
                              RequestContext(request))

  if request.method == 'POST' :
    station_id = request.POST.get('station')
    complaint_type = request.POST.get('complaint_type')
    complaint = Complaint.objects.get(id = complaint_id)
    station = Station.objects.get(id = request.POST.get('station'))
    complaint.station = station
    update_desc = 'Assigned to Station ' + station.district
    AddUpdateToDb(request.user, complaint, update_desc)
    complaint.complaint_type = complaint_type
    complaint.save()
    return ViewComplaint(request, complaint_id)

  c = Complaint.objects.all()[4]
  context_dict['complaint'] = c

def Register(request) :
  context = RequestContext(request)
  registered = False
  # If it's a HTTP POST, we're interested in processing form data.
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    if user_form.is_valid() :
      # Save the user's form data to the database.
      user = user_form.save()
      # to hash the password
      user.set_password(user.password)
      user.save()
      registered = True
    else:
      print user_form.errors
  else:
    user_form = UserForm()

  return render_to_response(
    'sos_action/register.html',
    {'user_form': user_form, 'registered': registered},
    context)  

@login_required(login_url='/sos_action/login')
def UserLogout(request):
  logout(request)
  return HttpResponseRedirect('/sos_action/')

def ListComplaints(request) :
  context = RequestContext(request)
  context_dict = {}
  context_dict['complaints'] = Complaint.objects.all()
  return render_to_response('sos_action/list_complaints.html', context_dict, context)

def ViewComplaint(request, complaint_id) :
  context = RequestContext(request)
  context_dict = {}
  context_dict['complaint'] = Complaint.objects.get(id = complaint_id)
  return render_to_response('sos_action/complaint.html', context_dict, context)

