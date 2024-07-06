from django.contrib import admin
from doctor.models import *
# Register your models here.

admin.site.register(specialities)

admin.site.register(doctor)

admin.site.register(dr_service_schedule)