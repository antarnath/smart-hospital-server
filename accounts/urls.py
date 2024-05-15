from django.urls import path, include 
from .views import *

urlpatterns = [
  path('register/', RegisterUser.as_view(), name='register'),
  path('verify/<str:email>/', VerifyUserEmail.as_view(), name='verify'),
  path('login/', LoginUser.as_view(), name='login'),
  path('profile/', UserProfile.as_view(), name='profile'), 
  path('password-reset/', PasswordResetRequest.as_view(), name='password-reset'),
  path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm')
] 