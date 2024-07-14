from rest_framework import serializers
from .models import *
from doctor.models import Doctor, Specialities
from rest_framework.exceptions import ValidationError
from django.core.serializers import serialize

class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['name', 'doctor', 'services', 'phone_number', 'date']
  
  def validate(self, data):
    doctor = data.get('doctor')
    services = data.get('services')
    date = data.get('date')
    name = data.get('name')
    phone_number = data.get('phone_number')
    request = self.context.get('request')
    # Check if the appointment already exists
    if Appointment.objects.filter(doctor=doctor, services=services, patient=request.user, date=date).exists():
        raise ValidationError('You have already booked an appointment')
    sp = Specialities.objects.filter(id=services.pk).first()
    
    # Increment doctor's number of patients
    doctor_info = Doctor.objects.filter(id=doctor.pk).first()
    if doctor_info.speciality.pk != sp.pk:
      raise ValidationError('Doctor is not available for this service')
    
    doctor_info.number_of_patients += 1
    doctor_info.save()
    serial_number = doctor_info.number_of_patients
    
    # appointment = Appointment.objects.create(
    #   name = name,
    #   phone_number = phone_number,
    #   doctor = doctor,
    #   services = services,
    #   patient = request.user,
    #   date = date,
    # )

    data['serial_number'] = serial_number
    data['doctor_info'] = {
      'name': doctor_info.name,
      'speciality': doctor_info.speciality.name,
      'email': doctor_info.email,
      'phone': doctor_info.phone,
      'address': doctor_info.address,
      'image': doctor_info.image.url,
      'description': doctor_info.description,
      'education': doctor_info.education,
      'passing_year': doctor_info.pasaing_year,
      'experience': doctor_info.experience,
      'fee': doctor_info.fee,
      'status': doctor_info.status,
    }
    return data

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['serial_number'] = self.validated_data.get('serial_number')
    data['doctor_info'] = self.validated_data.get('doctor_info')
    return data
