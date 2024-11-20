from rest_framework import serializers
from .models import *


class HospitalSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hospital
    fields = '__all__'
    
class SpecialitiesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Specialities
    fields = '__all__'
    
class DoctorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = '__all__'
    
    
from rest_framework_simplejwt.tokens import RefreshToken


# class LoginSerializer(serializers.ModelSerializer):
#   email = serializers.EmailField(max_length=255, min_length=6)
#   password = serializers.CharField(max_length=65, write_only=True)
#   access_token = serializers.CharField(max_length=255, read_only=True)
#   doctor = DoctorSerializer(read_only=True)
   
#   class Meta:
#     model = Doctor
#     fields = ['email', 'password', 'access_token', 'user']
  
#   def validate(self, attrs):
#     email = attrs.get('email')
#     password = attrs.get('password')
#     request = self.context.get('request')
#     user = authenticate(request, email=email, password=password)
#     if not user:
#       raise AuthenticationFailed({'message': 'Email or Password is incorrect'})
#     if not user.is_verified:
#       raise AuthenticationFailed({'message': 'Account is not verified'})
#     user_tokens = user.tokens()

#     return {
#       'email': user.email,
#       'access_token': str(user_tokens['access']),
#       'user': user
#     }
