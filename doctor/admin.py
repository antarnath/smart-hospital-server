from django.contrib import admin
from doctor.models import *
# Register your models here.

class SpecialitiesAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
admin.site.register(Specialities, SpecialitiesAdmin)

class DoctorAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
admin.site.register(Doctor, DoctorAdmin)
 
admin.site.register(Dr_service_schedule)

admin.site.register(Hospital)