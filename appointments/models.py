from django.db import models
from accounts.models import User
from doctor.models import Doctor, Specialities


# Create your models here.
class Appointment(models.Model):
  name = models.CharField(max_length=100)
  phone_number = models.CharField(max_length=15)
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  patient = models.ForeignKey(User, on_delete=models.CASCADE)
  services = models.ForeignKey(Specialities, on_delete=models.CASCADE)
  date = models.DateField()
  verify = models.BooleanField(default=False)
  
  
class Payment(models.Model):
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
  amount = models.IntegerField()
  transaction_id = models.IntegerField(default=10001)
  status = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.amount
  
  
  
class PaymentGateWaySettings(models.Model):
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)
  