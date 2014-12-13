from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request) :
  return HttpResponse("Welcome to Pukar Management System")
