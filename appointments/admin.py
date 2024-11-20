from django.contrib import admin
from .models import Appointment, PaymentGateWaySettings, Payment


admin.site.register(Appointment)    
admin.site.register(PaymentGateWaySettings)
admin.site.register(Payment)