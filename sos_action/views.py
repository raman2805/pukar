# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import *

def index(request) :
  context = RequestContext(request)
  return render_to_response('sos_action/index.html', {}, context)

def list_actions(request) :
  context = RequestContext(request)
  context_dict = {}
  context_dict['actions'] = Action.objects.all()
  return render_to_response('sos_action/list_actions.html', context_dict, context)

def list_complaints(request) :
  context = RequestContext(request)
  context_dict = {}
  context_dict['complaints'] = Complaint.objects.all()
  return render_to_response('sos_action/list_complaints.html', context_dict, context)

def view_complaint(request, id) :
  context = RequestContext(request)
  context_dict = {}
  complaint_id = id
  complaint = Complaint.objects.get(id = complaint_id)
  actions = Action.objects.filter(complaint_id = complaint_id)
  context_dict['complaint'] = complaint
  context_dict['actions'] = actions
  return render_to_response('sos_action/complaint.html', context_dict, context)

def add_action(request, complaint_id = -1) :
  context = RequestContext(request)
  context_dict = {}
  for key, val in request.GET.iteritems() :
    context_dict[key] = val

  if request.method == 'POST':
    form = ActionForm(request.POST)
      # Have we been provided with a valid form?
    if form.is_valid() :
      action = form.save(commit=False)
      action.complaint_id = complaint_id
      action.save()
      return view_complaint(request, action.complaint_id)
    else :
      return HttpResponse(form.errors)

  # process the get parameter, insert the complaint and then process the action
  elif complaint_id != -1 :
    form = ActionForm()
      # adding action given complaint_id 
    try :
      c = Complaint.objects.get(id = complaint_id)
      context_dict['complaint'] = c
    except ValueError :
      return HttpResponse("Sorry, could not process the complaint, it does not exist in the DB ")

  else :
    import datetime 
    c = Complaint()
    c.name = request.GET.get('name')
    c.mobile = request.GET.get('mobile')
    c.location = request.GET.get('location', '')
    c.complaint_time = request.GET.get('time', datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S'))
    c.imei = request.GET.get('imei', '')
    c.status = 'PENDING'
    c.save()
    return add_action(request, c.id)
    # first save the complaint
    # add the action
        
  context_dict['form'] = form

  # Bad form (or form details), no form supplied...
  # Render the form with error messages (if any).
  return render_to_response('sos_action/add_action.html', 
                            context_dict, 
                            context)
