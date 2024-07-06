from django.urls import path
from .views import *

urlpatterns = [
    path('google/', GoogleSignInView.as_view(), name='google')
]
