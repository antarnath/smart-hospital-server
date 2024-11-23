from django.urls import path, include
from .views import * 

urlpatterns = [
  path('', make_appointment.as_view(), name='make_appointment'),
  path('payment/', Payment.as_view(), name='payment'),
  path('payment/success/<int:id>/', Payment_success.as_view(), name='payment-success'),
  path('payment-confirmation/', PaymentConfirmation.as_view(), name='payment-confirmation'),
  path('get-appointment/<int:appointment_id>/', GetAppointment.as_view(), name='get-appointments'),
  path('all-appointments/', AllAppointments.as_view(), name='all-appointments'),
  path('submit-report/<int:id>/', SubmitReport.as_view(), name='submit-report'),
] 