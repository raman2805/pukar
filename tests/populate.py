import csv
import os

if __name__ == '__main__' :
  os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'pukar.settings')
  from sos_action.models import *
  with open('tests/complaint.csv', 'r') as csvfile :
    reader = csv.reader(csvfile)
    for row in reader :
      if row[0] == 'name' :
        continue
      c = Complaint()
      c.name = row[0]
      c.mobile = row[1]
      c.imei = row[2]
      c.location = row[3]
      c.complaint_time = row[4]
      c.save()

  with open('tests/actions.csv', 'r') as csvfile :
    reader = csv.reader(csvfile)
    for row in reader :
      if row[1] == 'name' :
        continue
      a = Action()
      a.complaint_id = row[0]
      a.name = row[1]
      a.action = row[2]
      a.save()

