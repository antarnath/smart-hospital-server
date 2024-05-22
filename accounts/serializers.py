from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
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
      raise serializers.ValidationError({'email': 'Email is already in use'})
    
    user = User.objects.create(
      email=email,
      first_name=first_name,
      last_name=last_name,
      phone_number=phone_number
    )
    user.set_password(password)
    user.save()
    return user
  
class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=6)
  password = serializers.CharField(max_length=65, write_only=True)
  full_name = serializers.CharField(max_length=255, read_only=True)
  access_token = serializers.CharField(max_length=255, read_only=True)
  
  class Meta:
    model = User
    fields = ['email', 'password', 'full_name', 'access_token']
  
  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    request = self.context.get('request')
    user = authenticate(request, email=email, password=password)
    if not user:
      raise AuthenticationFailed('Email or Password is incorrect')
    if not user.is_verified:
      raise AuthenticationFailed('Account is not verified')
    user_tokens = user.tokens()
    
    return {
      'email': user.email,
      'full_name': user.get_full_name,
      'access_token': str(user_tokens['access'])
    }

class PasswordResetRequestSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=6)
  
  class Meta:
    model = User
    fields = ['email']
    
  def validate(self, attrs):
    email = attrs.get('email') 
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      request = self.context.get('request')
      current_site = get_current_site(request).domain
      relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
      abslink = f"http://{current_site}{relative_link}"
      email_body = f"Hi {user.first_name} use the link below to reset your password \n {abslink}"
      data = {
        'email_body': email_body,
        'email_subject': 'Reset your password', 
        'to_email': user.email
      }
      send_normal_email(data)
      attrs['uidb64'] = uidb64
      attrs['token'] = token
    return attrs
  def to_representation(self, instance):
    ret = super().to_representation(instance)
    ret['uidb64'] = self.validated_data.get('uidb64')
    ret['token'] = self.validated_data.get('token')
    return ret
  
class PasswordResetConfirmSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=255, min_length=8, write_only=True)
  
  class Meta:
    model = User
    fields = ['password']
  
  def validate(self, attrs):
    try:
      password = attrs.get('password')
      uidb64 = self.context.get('uidb64')
      token = self.context.get('token')
      user_id = smart_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=user_id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise AuthenticationFailed('The reset link is invalid', 401)
      user.set_password(password)
      user.save()
      return user
    except DjangoUnicodeDecodeError as identifier:
      raise AuthenticationFailed('The reset link is invalid', 401)
    
    
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'phone_number']