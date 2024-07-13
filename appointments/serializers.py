from rest_framework import serializers
from .models import *
from doctor.models import Doctor, Specialities
from rest_framework.exceptions import ValidationError

class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['name', 'doctor', 'services', 'phone_number', 'date']
    
  def validate(self, data):
    doctor = data.get('doctor')
    services = data.get('services')
    date = data.get('date')
    request = self.context.get('request')
    if Appointment.objects.filter(doctor=doctor, services=services, patient=request.user, date=date).exists():
      raise ValidationError('You have already booked an appointment') 
    appointment = Appointment.objects.create( 
      doctor=doctor,
      services=services,
      patient=request.user,
      date=date, 
    )
    doctor.number_of_patients += 1
    serial_number = doctor.number_of_patients
    data['serial_number'] = serial_number
    data['doctor_name'] = doctor.name
    print(doctor.name)
    return data
  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['serial_number'] = self.validated_data.get('serial_number')
    data['doctor_name'] = self.validated_data.get('doctor_name')
    return data