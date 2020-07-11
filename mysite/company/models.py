from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
