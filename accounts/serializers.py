from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.encoding import smart_bytes, smart_str, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from django.utils.encoding import DjangoUnicodeDecodeError


class UserRegisterSerializers(serializers.ModelSerializer):
  password = serializers.CharField(max_length=255, min_length=8, write_only=True)
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'phone_number', 'password']
  
  def create(self, validated_data):
    email = validated_data['email']
    first_name = validated_data['first_name']
    last_name = validated_data['last_name']
    phone_number = validated_data['phone_number']
    password = validated_data['password']
    
    if User.objects.filter(email=email).exists():
      raise serializers.ValidationError({'message': 'Email is already in use'})
    
    user = User.objects.create(
      email=email,
      first_name=first_name,
      last_name=last_name,
      phone_number=phone_number
    )
    user.set_password(password)
    user.save()
    return user
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
    
    
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation.pop('password', None)
    return representation
  
class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=6)
  password = serializers.CharField(max_length=65, write_only=True)
  access_token = serializers.CharField(max_length=255, read_only=True)
  user = UserSerializer(read_only=True)
   
  class Meta:
    model = User
    fields = ['email', 'password', 'access_token', 'user']
  
  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    request = self.context.get('request')
    user = authenticate(request, email=email, password=password)
    if not user:
      raise AuthenticationFailed({'message': 'Email or Password is incorrect'})
    if not user.is_verified:
      raise AuthenticationFailed({'message': 'Account is not verified'})
    user_tokens = user.tokens()

    return {
      'email': user.email,
      'access_token': str(user_tokens['access']),
      'user': user
    }




class ForgotPasswordSerializer(serializers.Serializer):
  email = serializers.EmailField()

  def validate_email(self, value):
    if not User.objects.filter(email=value).exists():
      raise serializers.ValidationError("No user is associated with this email.")
    return value
  


  
class SetNewPasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=255, min_length=8, write_only=True)
  email = serializers.EmailField()
  
  class Meta:
    model = User
    fields = ['email', 'password']
  
  def validate(self, attrs):
    try:
      email = attrs.get('email')
      password = attrs.get('password')
      user = User.objects.get(email=email)
      user.set_password(password)
      user.save()
      return user
    except Exception as e:
      raise AuthenticationFailed({'message': 'password and user is invalid'}, 401)
      
    
    
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'phone_number']