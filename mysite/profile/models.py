from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)


class Manager(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, date_created=timezone.now(), date_updated=timezone.now())


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.date_updated = timezone.now()
    instance.profile.save()
