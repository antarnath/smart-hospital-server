from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from rest_framework import status
from .ssl import sslcommerz_payment_gateway


class make_appointment(GenericAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = AppointmentSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
  

  
class Payment(GenericAPIView):
  def post(self, request):
    name = request.data.get('name')
    amount = request.data.get('amount')

    if not name or not amount:
      return Response({'error': 'Name and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    payment_url = sslcommerz_payment_gateway(request, name, amount)
    return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
