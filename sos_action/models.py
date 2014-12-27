from django.db import models
import django.contrib.auth.models
from pukar.settings import DATA_PATH
# Create your models here.
# different naming convention here (to comply with Ravi's notation)
import os
gComplaintTypes = []
with open(os.path.join(DATA_PATH, 'raw', 'complaint_types.csv')) as fd :
  complaint_list = fd.read().split('\n')[:-1]
  gComplaintTypes = [(x, x) for x in complaint_list]

class mobappuser(models.Model) : 
  userName = models.CharField(max_length = 10)
  userPhoneNo = models.CharField(max_length = 10)
  imeiNo = models.CharField(max_length = 128)
  userEmail = models.CharField(max_length = 128)
  emergencyPh1 = models.CharField(max_length = 10)
  emergencyPh2 = models.CharField(max_length = 10)
  emergencyPh3 = models.CharField(max_length = 10)
  emergencyPh4 = models.CharField(max_length = 10)
  emergencyPh5 = models.CharField(max_length = 10)
  createDate = models.DateTimeField(null = False)
  lastUpdate =  models.DateTimeField(null = True)
  def __unicode__(self) : 
    return self.userName + ' ' + self.userPhoneNo

class Station(models.Model) :
  range = models.CharField(max_length = 128)
  district = models.CharField(max_length = 128)
  station = models.CharField(max_length = 128)
  type = models.CharField(max_length = 128)
  in_charge = models.CharField(max_length = 128)
  contact = models.CharField(max_length = 128)

class Complaint(models.Model) :
  complainant = models.ForeignKey(mobappuser)
  station = models.ForeignKey(Station, null = True)
  complaint_type = models.CharField(max_length = 128,
                                    choices = gComplaintTypes,
                                    null = True)
  location = models.CharField(max_length = 30)
  location_link = models.CharField(max_length = 128)
  complaint_time = models.DateTimeField()
  informer = models.CharField(max_length = 128, null = True)
  resolved_time = models.DateTimeField(null = True)
  status = models.CharField(max_length = 10,
                            choices = [('OPEN', 'OPEN'), 
                                       ('CLOSED', 'CLOSED')])
  def __unicode__(self) : 
    return self.complainant.userName

class Updates(models.Model) :
  user = models.ForeignKey(django.contrib.auth.models.User)
  complaint = models.ForeignKey(Complaint)
  update_time = models.DateTimeField(auto_now_add = True) 
  information = models.CharField(max_length = 1000)
