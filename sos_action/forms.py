from django import forms
from models import Complaint
from django.contrib.auth.models import User
from sos_action.models import gComplaintTypes

#gAllUsers = ('All', 'All') + 
#            [(x.userName, x.id) for x in User.objects.all()]
#
#gAllDistricts = [('All', 'All')] + 
#                [(x.district, x.district) for x in Station.objects.all()]
#
class UserForm(forms.ModelForm) :
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ('username', 'email', 'password')
