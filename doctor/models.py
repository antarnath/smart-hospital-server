from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    


class Specialities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=1)
    speciality = models.ForeignKey(Specialities, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='doctor/images/')
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

