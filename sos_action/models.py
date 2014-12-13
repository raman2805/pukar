from django.db import models

# Create your models here.
class Complaint(models.Model) :
  name = models.CharField(max_length = 128)
  mobile = models.CharField(max_length = 10)
  imei = models.CharField(max_length = 15)
  location = models.CharField(max_length = 30)
  complaint_time = models.DateTimeField()
  status = models.CharField(max_length = 10,
                            choices = (('N', 'NEW'), 
                                       ('A', 'ACTING'), 
                                       ('R', 'RESOLVED' )))
  def __unicode__(self) : 
    return self.mobile

class Action(models.Model) :
  complaint = models.ForeignKey(Complaint)
  name = models.CharField(max_length = 128)
  action_time = models.DateTimeField(auto_now_add = True)
  action = models.CharField(max_length = 128)
  def __unicode__(self) : 
    return self.name
