from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from django.views import View
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .ssl import sslcommerz_payment_gateway
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class make_appointment(GenericAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = AppointmentSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
  

  
class Payment(GenericAPIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    user = request.user 
    amount = request.data.get('amount')
    appointment_id = request.data.get('appointment_id')
    doctor_id = request.data.get('doctor_id')
    appointment = Appointment.objects.filter(id=appointment_id).first()
    doctor = Doctor.objects.filter(id=doctor_id).first()
    
    
 
    if not appointment_id and not amount:
      return Response({'error': 'appointment id and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    payment_url = sslcommerz_payment_gateway(request, user, amount, appointment, doctor)
    return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
  
@method_decorator(csrf_exempt, name='dispatch')
class Payment_success(GenericAPIView):
  serializer_class = PaymentSuccessSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
