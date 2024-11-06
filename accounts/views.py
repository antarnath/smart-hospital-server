from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .utils import send_code_to_user
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
import random
from django.conf import settings
from django.core.mail import EmailMessage

class RegisterUser(GenericAPIView):
  serializer_class = UserRegisterSerializers
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
      serializer.save()
      user = serializer.data
      # send One Time Password to user email
      send_code_to_user(user['email'])
      return Response({
        'email': user['email'],   
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
      
class LoginUser(GenericAPIView):
  serializer_class = LoginSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
  
class UserProfile(GenericAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = UserProfileSerializer

  def get(self, request):
      users = request.user
      serializer = self.get_serializer(users)
      return Response({
          'message': 'User Profile Page',
          'user': serializer.data
      }, status=status.HTTP_200_OK)
    
    
def generateOtp():
  otp = ""
  for i in range(6):
    otp += str(random.randint(1, 9))
  return otp
class ForgetPassword(GenericAPIView):
  serializer_class = ForgotPasswordSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
      
    email = serializer.validated_data['email']
    user = User.objects.get(email=email)
    
    otp = generateOtp()
    OneTimePasswordForForgetPassword.objects.create(user=user, code=otp)
    
    subject = "Forget Password"
    email_body = f'Hi {user.first_name} This is your OTP {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_email = EmailMessage(
      subject=subject,
      body=email_body,
      from_email=from_email,
      to=[email]
    )
    send_email.send(fail_silently=True)
    
    return Response({"message": "OTP sent to email successfully."}, status=status.HTTP_200_OK)
    
    
class ForgetPasswordVerify(GenericAPIView):
  def post(self, request, email):
    otp = request.data.get('otp')
    user = User.objects.get(email=email)
    try:
      otp_obj = OneTimePasswordForForgetPassword.objects.get(user=user)
    except OneTimePasswordForForgetPassword.DoesNotExist:
      return Response({
        'message': 'No OTP found'
      }, status=status.HTTP_400_BAD_REQUEST)
      
    if otp == otp_obj.code:
      otp_obj.delete()
      return Response({
        'message': 'OTP Verified',
        'email': email
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'message': 'Invalid OTP'
      }, status=status.HTTP_400_BAD_REQUEST)
    

      
class SetNewPassword(GenericAPIView):
  serializer_class = SetNewPasswordSerializer
  
  def patch(self, request):
    serializers = self.serializer_class(data=request.data)
    serializers.is_valid(raise_exception=True)
    return Response({
      'message': 'Password reset successful'
    }, status=status.HTTP_200_OK)