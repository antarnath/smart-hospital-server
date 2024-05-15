from django.urls import path, include 
from .views import *

urlpatterns = [
  path('register/', RegisterUser.as_view(), name='register'),
  path('verify/<str:email>/', VerifyUserEmail.as_view(), name='verify'),
] 