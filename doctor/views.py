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
      "specialities": SpecialitiesSerializer(specialities, many=True).data
    }

    return Response(response_data, status=status.HTTP_200_OK)

class AllHospital(APIView):
  def get(self, request, *args, **kwargs):
    hospitals = Hospital.objects.all()
    response_data = {
      "hospitals": HospitalSerializer(hospitals, many=True).data,
    }

    return Response(response_data, status=status.HTTP_200_OK)
  
class AllSpecialities(APIView):
  def get(self, request, *args, **kwargs):
    specialities = Specialities.objects.all()
    response_data = {
      "specialities": SpecialitiesSerializer(specialities, many=True).data,
    }

    return Response(response_data, status=status.HTTP_200_OK)
  
class AllDoctor(APIView):
  def get(self, request, *args, **kwargs):
    doctors = Doctor.objects.all()
    response_data = {
      "doctors": DoctorSerializer(doctors, many=True).data,
    }

    return Response(response_data, status=status.HTTP_200_OK)
  
  
class DoctorsByHospital(APIView):
  def get(self, request, id, *args, **kwargs):
    try:
      hospital = Hospital.objects.get(id=id)
    except Hospital.DoesNotExist:
      return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)
    
    doctors = Doctor.objects.filter(hospital=hospital)
    response_data = {
      "doctors": DoctorSerializer(doctors, many=True).data,
    }
    return Response(response_data, status=status.HTTP_200_OK)
    
class DoctorsBySpeciality(APIView):
  def get(self, request, id, *args, **kwargs):
    try:
      speciality = Specialities.objects.get(id=id)
    except Specialities.DoesNotExist:
      return Response({"error": "Speciality not found"}, status=status.HTTP_404_NOT_FOUND)
    
    doctors = Doctor.objects.filter(speciality=speciality)
    response_data = {
      "doctors": DoctorSerializer(doctors, many=True).data,
    }
    return Response(response_data, status=status.HTTP_200_OK)