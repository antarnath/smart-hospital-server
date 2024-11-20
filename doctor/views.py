from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from.serializers import *
from rest_framework.response import Response
from rest_framework import status


class Home(APIView):
  def get(self, request, *args, **kwargs):
    hospitals = Hospital.objects.all()[:10]
    specialities = Specialities.objects.all()[:10]
    doctors = Doctor.objects.all()[:10]

    response_data = {
      "hospitals": HospitalSerializer(hospitals, many=True).data,
      "specialities": SpecialitiesSerializer(specialities, many=True).data,
      "doctors": DoctorSerializer(doctors, many=True).data,
    }

    return Response(response_data, status=status.HTTP_200_OK) 
  
  

class SearchView(APIView):
  def get(self, request, *args, **kwargs):
    search_query = request.query_params.get('search', None)  # Get the search input

    if not search_query:
      return Response({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Search Hospitals
    hospitals = Hospital.objects.filter(name__icontains=search_query)

    # Search Doctors
    doctors = Doctor.objects.filter(name__icontains=search_query)

    # Search Specialities and retrieve related doctors
    specialities = Specialities.objects.filter(name__icontains=search_query)
    doctors_by_speciality = Doctor.objects.filter(speciality__in=specialities)

    # Serialize the results
    response_data = {
      "hospitals": HospitalSerializer(hospitals, many=True).data,
      "doctors": DoctorSerializer(doctors, many=True).data,
      "doctors_by_speciality": DoctorSerializer(doctors_by_speciality, many=True).data, 
    }

    return Response(response_data, status=status.HTTP_200_OK)
