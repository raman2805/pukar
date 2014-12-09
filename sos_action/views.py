# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
  return HttpResponse("Rango says hello world!")


def index(request):
  context = RequestContext(request)
  context_dict = {'name': "Raman"}
  return render_to_response('sos_action/index.html', context_dict, context)
