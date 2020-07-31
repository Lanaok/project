from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils import timezone

from profile.models import Profile, Manager


class Company(models.Model):
    class CompanyType(models.TextChoices):
        RESTAURANT = 'RE', 'Restaurant'
        HOSPITAL = 'HO', 'Hospital'
        DENTISTRY = 'DE', 'Dentistry'
        BEAUTY_SALOON = 'BE', 'Beauty Salon'

    name = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    company_type = models.CharField(choices=CompanyType.choices, max_length=10)

    class Meta:
        permissions = (("can_edit_company", "Edit company info"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])


class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    photos = models.ImageField()
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    duration = models.DurationField(default=timedelta(days=0))
    image = models.ImageField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.profile.user.username
