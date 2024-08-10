from django.db import models


class Specialities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.ForeignKey(Specialities, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(upload_to='doctor/images/')
    description = models.TextField()
    education = models.TextField()
    passing_year = models.CharField(max_length=4)
    experience = models.CharField(max_length=2)
    fee = models.IntegerField()
    status = models.BooleanField(default=True)
    number_of_patients = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Dr_service_schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    sunday = models.CharField(max_length=60, default='Closed')
    monday = models.CharField(max_length=60, default='Closed')
    tuesday = models.CharField(max_length=60, default='Closed')
    wednesday = models.CharField(max_length=60, default='Closed')
    thursday = models.CharField(max_length=60, default='Closed')
    friday = models.CharField(max_length=60, default='Closed')
    saturday = models.CharField(max_length=60, default='Closed')

    def __str__(self):
        return self.doctor.name

