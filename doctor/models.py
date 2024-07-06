from django.db import models

# Create your models here.

class specialities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.ForeignKey(specialities, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(upload_to='doctor/images/')
    description = models.TextField()
    education = models.TextField()
    pasaing_year = models.CharField(max_length=4)
    experience = models.CharField(max_length=2)
    fee = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class dr_service_schedule(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    sunday = models.CharField(max_length=60, default='Closed')
    monday = models.CharField(max_length=60, default='Closed')
    tuesday = models.CharField(max_length=60, default='Closed')
    wednesday = models.CharField(max_length=60, default='Closed')
    thursday = models.CharField(max_length=60, default='Closed')
    friday = models.CharField(max_length=60, default='Closed')
    saturday = models.CharField(max_length=60, default='Closed')

    def __str__(self):
        return self.doctor.name
