from django.db import models
from allauth.account.signals import user_logged_in
from django.contrib.auth import  get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




def user_logged_in_receiver(request, user, **kwargs):
   return user







