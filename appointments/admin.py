from django.contrib import admin
from .models import Appointment, PaymentGateWaySettings, Payment

class AppintmentModel(admin.ModelAdmin):
  list_display = ['id', 'name']
admin.site.register(Appointment, AppintmentModel)    
admin.site.register(PaymentGateWaySettings)
admin.site.register(Payment)