from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from.serializers import *
from rest_framework.response import Response
from rest_framework import status


class Home(APIView):
  def get(self, request, *args, **kwargs):
    hospitals = Hospital.objects.all()
    specialities = Specialities.objects.all()
    doctors = Doctor.objects.all()

    response_data = {
      "hospitals": HospitalSerializer(hospitals, many=True).data,
      "specialities": SpecialitiesSerializer(specialities, many=True).data,
      "doctors": DoctorSerializer(doctors, many=True).data,
    }

    return Response(response_data, status=status.HTTP_200_OK) 