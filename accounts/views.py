from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .utils import send_code_to_user


class RegisterUser(GenericAPIView):
  serializer_class = UserRegisterSerializers
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      user = serializer.data
      # send One Time Password to user email
      send_code_to_user(user['email'])
      return Response({
        'user': user,
        'message': f'hi {user["first_name"]}, please check your email for the OTP'
      }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class VerifyUserEmail(GenericAPIView):
  def post(self, request, email):
    otp = request.data.get('otp')
    user = User.objects.get(email=email)
    if user.is_verified:
      return Response({
        'message': 'Email is already verified'
      }, status=status.HTTP_400_BAD_REQUEST)
    otp_obj = OneTimePassword.objects.get(user=user)
    if otp == otp_obj.code:
      user.is_verified = True
      user.save()
      otp_obj.delete()
      return Response({
        'message': 'Email Verified'
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'message': 'Invalid OTP'
      }, status=status.HTTP_400_BAD_REQUEST)