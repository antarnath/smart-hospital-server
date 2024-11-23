from rest_framework import serializers
from .models import *
from doctor.models import Doctor, Specialities
from rest_framework.exceptions import ValidationError
from django.core.serializers import serialize


class AppointmentModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['doctor','date']
  
  def validate(self, data):
    doctor = data.get('doctor')
    date = data.get('date')
    request = self.context.get('request')
    doctor_info = Doctor.objects.filter(id=doctor.pk).first()
    cnt = Appointment.objects.filter(doctor=doctor, date=date, verify=True).count()
    if cnt >= 50:
      raise ValidationError('Doctor is not available')
    
    # Check if the appointment already exists
    if Appointment.objects.filter(doctor=doctor, patient=request.user, date=date).exists():
        raise ValidationError('You have already booked an appointment')
    
    
    doctor_info.number_of_patients += 1
    doctor_info.save()
    serial_number = doctor_info.number_of_patients
    
    appointment = Appointment.objects.create(
      doctor = doctor,
      patient = request.user,
      date = date,
    )
    print(appointment.verify)
    print(appointment.id)
    data['appointment_id'] = appointment.id
    data['serial_number'] = serial_number
    data['payment_status'] = appointment.verify
    data['doctor_info'] = {
      'id': doctor_info.id,
      'name': doctor_info.name,
      'speciality': doctor_info.speciality.name,
      'email': doctor_info.email,
      'phone': doctor_info.phone,
      'image': doctor_info.image.url,
      'education': doctor_info.education,
      'passing_year': doctor_info.passing_year,
      'experience': doctor_info.experience,
      'fee': doctor_info.fee,
      'status': doctor_info.status,
    }
    return data

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['serial_number'] = self.validated_data.get('serial_number')
    data['doctor_info'] = self.validated_data.get('doctor_info')
    data['appointment_id'] = self.validated_data.get('appointment_id')
    data['payment_status'] = self.validated_data.get('payment_status')
    return data



class PaymentSuccessSerializer(serializers.Serializer):
  tran_id = serializers.CharField(required=True)
  val_id = serializers.CharField(required=True)
  amount = serializers.CharField(required=True)
  card_type = serializers.CharField(required=True)
  store_amount = serializers.CharField(required=True)
  status = serializers.CharField(required=True)
  tran_date = serializers.CharField(required=True)
  currency = serializers.CharField(required=True)
  value_a = serializers.CharField(required=True)
  value_b = serializers.CharField(required=True)
  value_c = serializers.CharField(required=True)
  value_d = serializers.CharField(required=True)
  def validate(self, data):
    print("==========================")
    print(data)
    user = data.get('value_a')
    amount = data.get('value_b')
    appointment = data.get('value_c')
    doctor = data.get('value_d')
    print(user, amount, appointment, doctor) 
    return data
  
  
class PaymentConfirmationSerializer(serializers.Serializer):
  id = serializers.IntegerField(required=True)
  
  def validate(self, data):
    print(data['id'])
    appointment_id = data['id']
    appointment = Appointment.objects.filter(id=appointment_id).first()
    appointment.verify = True
    appointment.save()
    return data 
  


class SubmitReportSerializer(serializers.Serializer):
  report = serializers.ImageField(required=True)
  def validate(self, data):
    report = data.get('report')
    appointment_id = self.context.get('id')
    appointment = Appointment.objects.filter(id=appointment_id).first()
    appointment.report = report
    appointment.save()
    print(report)
    if not report:
      raise ValidationError('report is required')
    return data