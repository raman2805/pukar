import csv
import os
import sys
def get_random_time()  :
  import random
  return '%02d:%02d:%02d' % (random.randint(0, 23),
                            random.randint(0, 59),
                            random.randint(0, 59))

def get_random_date()  :
  import random
  return '%04d-%02d-%02d' % (random.randint(2010, 2013),
                             random.randint(1, 12),
                             random.randint(1, 28))


def PopMobAppUser() :
  import random
  first = [ 'Ramesh', 'Aditya', 'Shashank', 'Ravi', 'Alan', 'Sudeep', 'Ankit', 'Roxy', 'Sanya' ]
  last = [ 'Gupta', 'Mittal', 'Bansal', 'Arora', 'Malhotra' ]
  from sos_action.models import mobappuser
  [ x.delete for x in mobappuser.objects.all() ]
  for i in range(100) :
    u = mobappuser()
    u.userName = random.choice(first) + ' ' + random.choice(last)
    u.userPhoneNo = random.randint(9000000000, 9999999999)
    u.imeiNo = random.randint(9000000000, 9999999999)
    u.emergencyPh1 = random.randint(9000000000, 9999999999)
    u.emergencyPh2 = random.randint(9000000000, 9999999999)
    u.emergencyPh3 = random.randint(9000000000, 9999999999)
    u.emergencyPh4 = random.randint(9000000000, 9999999999)
    u.emergencyPh5 = random.randint(9000000000, 9999999999)
    u.createDate = get_random_date() + ' ' + get_random_time()
    u.lastUpdate = get_random_date() + ' ' + get_random_time()
    u.save()

def PopStations(inputFile) :
  from sos_action.models import Station
  [ x.delete for x in Station.objects.all() ]
  with open(inputFile, 'r') as csvfile :
    reader = csv.reader(csvfile)
    count = 0
    for row in reader :
      print 'processing',  row
      # to exclude the header
      if 'range' in row :
          continue
      s = Station()
      (s.range, s.district, s.station, s.type, s.in_charge, s.contact) = tuple(row)
      s.save()

def PopComplaints() :
  from sos_action.models import Complaint, mobappuser, Station
  import random
  [ x.delete for x in Complaint.objects.all() ]
  districts = [ x.district for x in Station.objects.all()]
  user_ids = [ x.id for x in mobappuser.objects.all() ]
  informers = [ 'Abhijat', 'Ronald', 'Dhani' ]
  for i in range(20) :
      c = Complaint()
      c.complainant = random.choice(mobappuser.objects.all())
      c.location = random.choice(districts)
      c.complaint_time = get_random_date() + ' ' + get_random_time()
      c.location_link = "https://www.google.co.uk/maps/dir//22.7077697,75.8588391/@22.7073738,75.8612316,16z"
      if random.randint(0, 10) > 7 :
        c.informer = random.choice(informers)
      c.status = 'OPEN'
      c.save()

def PopActions(inputFile) :
  from sos_action.models import Action
  with open(inputFile, 'r') as csvfile :
    reader = csv.reader(csvfile)
    for row in reader :
      if row[1] == 'name' :
        continue
      a = Action()
      a.complaint_id, a.name, a.action = tuple(row)
      a.save()

if __name__ == '__main__' :
  os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'pukar.settings')
  from sos_action.models import *
  from pukar.settings import *
  print DATA_PATH
  PopMobAppUser()
  PopStations(os.path.join(DATA_PATH, 'munged', 'stations.csv'))
  PopComplaints()
  #PopAction(os.path.join(DATA_PATH, 'raw', 'actions.csv'))
