# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import *
import models
from models import mobappuser, Station, Complaint, Updates
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import django
import sos_action
import datetime
import pytz
gRanges = list(set([x.range for x in Station.objects.all()]))
gComplaintTypesList = [x[0] for x in sos_action.models.gComplaintTypes]
gAllDistricts = list(set([x.district for x in Station.objects.all()]))

def index(request) :
  context = RequestContext(request)
  return render_to_response('sos_action/index.html', {}, context)

def AddUpdateToDb(user, complaint, information) :
  update = Updates()
  update.user = user
  update.complaint = complaint
  update.information = information
  update.save()

class Stat :
  pass

def GetStat(complaints) :
  stat = Stat()
  stat.open = len([x for x in complaints if x.status == 'OPEN' ])
  stat.closed = len([x for x in complaints if x.status != 'OPEN' ])
  resolved_times = [(x.resolved_time - x.complaint_time).days
                    for x in complaints if x.resolved_time]
  if resolved_times :
    stat.avg_resolution_time = int(sum(resolved_times)/len(resolved_times))
  return stat

def GetStats(complaints) :
  stats  = []
  stat = Stat()
  stat = GetStat(complaints)
  stat.type = 'Overall'
  stats.append(stat)

  for complaint_type in gComplaintTypesList :
    by_incident = [x for x in complaints if x.complaint_type == complaint_type]
    stat = GetStat(by_incident)
    stat.type = complaint_type
    stats.append(stat)

  unknown = [x for x in complaints if not x.complaint_type ]
  stat = GetStat(unknown)
  stat.type = 'Unknown'
  stats.append(stat)
  return stats



def Report(request) : 
  context = RequestContext(request)
  context_dict = {}
  context_dict['districts']  = gAllDistricts
  context_dict['users']  = django.contrib.auth.models.User.objects.all()
  complaints = Complaint.objects.all()
  district = request.GET.get('district', 'All')
  if district != 'All' :
    complaints = filter(lambda x : x.station and x.station.district == district, complaints)

  start_date = datetime.datetime.strptime(request.GET.get('start_date', '01-JAN-2001'), '%d-%b-%Y')
  today = datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y')
  end_date = datetime.datetime.strptime(request.GET.get('end_date', today), '%d-%b-%Y')
  
  if 'date_range' in request.GET :
    end_date = datetime.datetime.today()
    if request.GET.get('date_range') == 'week' : 
      start_date = end_date - datetime.timedelta(days = 7)
    elif request.GET.get('date_range') == 'month' : 
      start_date = end_date - datetime.timedelta(days = 30)

  start_date = pytz.utc.localize(start_date)
  end_date = pytz.utc.localize(end_date)
  complaints = filter(lambda x : x.complaint_time > start_date and x.complaint_time < end_date,
                      complaints)
  context_dict['stats'] = GetStats(complaints)
  context_dict['complaints'] = complaints
  context_dict['district'] = district
  context_dict['selected_start_date'] = datetime.datetime.strftime(start_date, '%d-%b-%Y')
  context_dict['selected_end_date'] = datetime.datetime.strftime(end_date, '%d-%b-%Y')

  # The filtering logic based on commands
  return render_to_response('sos_action/report.html', context_dict, context)

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
    context_dict['other_complaint_text'] = request.GET.get('other_complaint', '')
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
    if complaint.complaint_type == 'Others' : 
      complaint.complaint_type += ( ' - ' + request.POST.get('other_complaint', ''))
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

