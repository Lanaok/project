import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import Avg
from django.urls import reverse

from profile.models import Profile, Manager


class Company(models.Model):
    class CompanyType(models.TextChoices):
        RESTAURANT = 'RE', 'Restaurant'
        HOSPITAL = 'HO', 'Hospital'
        DENTISTRY = 'DE', 'Dentistry'
        BEAUTY_SALOON = 'BE', 'Beauty Salon'
        AUTO_SERVICE = 'AU', 'Auto Service'

    name = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    working_hour_from = models.TimeField(default=datetime.time(9, 00), null=False, blank=False)
    working_hour_to = models.TimeField(default=datetime.time(21, 00), null=False, blank=False)
    company_type = models.CharField(choices=CompanyType.choices, max_length=10)
    image = models.ImageField(null=True, blank=True, upload_to='company_photos/')

    class Meta:
        permissions = (("can_edit_company", "Edit company info"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])

    def average_review(self):
        reviews = Comment.objects.filter(company=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = int(reviews["avarage"])
        return avg


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
    image = models.ImageField(null=True, blank=True, upload_to='service_photos/')
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-view', args=[str(self.id)])


class StaffMember(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    date_joined = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(null=True, blank=True, upload_to='staff_photos/')

    def __str__(self):
        return self.profile.user.username

    def get_absolute_url(self):
        return reverse('staff-view', args=[str(self.id)])


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=100, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


