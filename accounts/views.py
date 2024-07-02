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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
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
    
class PasswordResetRequest(GenericAPIView):  
  serializer_class = PasswordResetRequestSerializer
  
  def post(self, request):
    serializer = self.get_serializer(data=request.data, context = {'request': request}) 
    serializer.is_valid(raise_exception=True)
    return Response({
      'data': serializer.data, 
      'message': 'Password reset link sent to your email'
    }, status=status.HTTP_200_OK)
    
    
# class PasswordResetConfirm(GenericAPIView):
#   serializer_class = PasswordResetConfirmSerializer
#   def patch(self, request, uidb64, token):
#     serializer = self.get_serializer(data=request.data, context={'request': request, 'uidb64': uidb64, 'token': token})
#     serializer.is_valid(raise_exception=True)
#     return Response({
#       'message': 'Password reset successful'
#     }, status=status.HTTP_200_OK) 
    
    
class PasswordResetConfirm(GenericAPIView):
  print("====================")
  print("====================")
  print("====================")
  print("====================")

  def get(self, request, uidb64, token):
    try:
      user_id = smart_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=user_id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        return Response(
          {'message': 'Token is invalid or expired. Please request a new one'},
          status=status.HTTP_400_BAD_REQUEST
        )
      return Response(
        {'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
        status=status.HTTP_200_OK
      )
    except DjangoUnicodeDecodeError as identifier:
      return Response(
        {'message': 'Token is invalid or expired. Please request a new one'},
        status=status.HTTP_400_BAD_REQUEST
      )
      
class SetNewPassword(GenericAPIView):
  serializer_class = SetNewPasswordSerializer
  
  def patch(self, request):
    serializers = self.serializer_class(data=request.data)
    serializers.is_valid(raise_exception=True)
    return Response({
      'message': 'Password reset successful'
    }, status=status.HTTP_200_OK)