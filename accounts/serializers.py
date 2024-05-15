from rest_framework import serializers
from .models import *


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