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
  