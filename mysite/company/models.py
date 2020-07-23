from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils import timezone

from profile.models import Profile, Manager


class Company(models.Model):
    Company_Type = (
        ('R', 'Restaurant/cafe'),
        ('M', 'Hospital/Dentistry'),
        ('S', 'Beauty Salon'),
    )
    name = models.CharField(max_length=50)
    manager = models.OneToOneField(Manager, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    company_type = models.CharField(max_length=1, choices=Company_Type, default='R')

    class Meta:
        permissions = (("can_edit_company", "Edit company info"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])


class Products(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=500)
    photos = models.ImageField()
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)


class Service(models.Model):
    service_name = models.CharField(max_length=50)
    service_description = models.TextField(max_length=200)
    service_price = models.IntegerField()
    service_duration = models.DurationField()
    service_image = models.ImageField()
    company = models.ManyToManyField(Company)


class StaffMember(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    date_joined = models.DateTimeField(default=timezone.now)
