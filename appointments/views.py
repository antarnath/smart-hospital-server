from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer
from rest_framework.response import Response


class make_appointment(GenericAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = AppointmentSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)