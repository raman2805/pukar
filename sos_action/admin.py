from django.contrib import admin
from sos_action.models import Complaint, Station, mobappuser

admin.site.register(Complaint)
admin.site.register(Station)
admin.site.register(mobappuser)
