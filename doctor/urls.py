from django.urls import path, include 
from .views import *

urlpatterns = [
  path('home/', Home.as_view(), name='home'),
  path('search/', SearchView.as_view(), name='search'), 
  path('all-hospital/', AllHospital.as_view(), name='all-hospital'),
  path('all-specialities/', AllSpecialities.as_view(), name='all-specialities'),
  path('all-doctor/', AllDoctor.as_view(), name='all-doctor'), 
  path('doctor-by-hospital/<int:id>/', DoctorsByHospital.as_view(), name='doctor-by-hospital'),
  path('doctor-by-speciality/<int:id>/', DoctorsBySpeciality.as_view(), name='doctor-by-speciality'),
] 