from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from company.models import Company

class Service(models.Model):
    service_name = models.CharField(max_length=50)
    service_description = models.TextField(max_length=200)
    service_price = models.IntegerField()
    service_duration = models.DurationField()
    service_image = models.ImageField()
    company_services = models.ManyToManyField(Company, through='Profile')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    staff_at = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL, blank=True, related_name="staff")
    staff_services = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL, blank=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, date_created=timezone.now(), date_updated=timezone.now())


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.date_updated = timezone.now()
    instance.profile.save()

