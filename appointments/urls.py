from django.urls import path, include
from .views import * 

urlpatterns = [
  path('', make_appointment.as_view(), name='make_appointment'),
  path('payment/', Payment.as_view(), name='payment')
] 