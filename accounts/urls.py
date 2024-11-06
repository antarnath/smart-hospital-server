from django.urls import path, include 
from .views import *

urlpatterns = [
  path('register/', RegisterUser.as_view(), name='register'),
  path('verify/<str:email>/', VerifyUserEmail.as_view(), name='verify'),
  path('login/', LoginUser.as_view(), name='login'),
  path('profile/', UserProfile.as_view(), name='profile'), 
  path('forget-password/', ForgetPassword.as_view(), name='forget-password'), 
  path('forget-password-verify/<str:email>/', ForgetPasswordVerify.as_view(), name='forget-password-verify'),
  path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
] 