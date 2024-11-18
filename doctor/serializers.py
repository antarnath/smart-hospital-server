from rest_framework import serializers
from .models import *


class HospitalSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hospital
    fields = '__all__'
    
class SpecialitiesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Specialities
    fields = '__all__'
    
class DoctorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = '__all__'


