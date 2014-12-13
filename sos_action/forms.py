from django import forms
from models import Complaint, Action

class ActionForm(forms.ModelForm) :
  name = forms.CharField(max_length = 128, 
                         help_text = 'Add Name of Person handling the complaint')
  action = forms.CharField(max_length = 128,
                           help_text = 'Action taken')
  complaint_id = forms.IntegerField(widget = forms.HiddenInput, initial = 4)

  class Meta :
    model = Action
    fields = ( 'name', 'action', 'complaint_id')

