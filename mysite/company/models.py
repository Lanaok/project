from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone




class Company(models.Model):
    Company_Type = (
        ('R', 'Restaurant/cafe'),
        ('M', 'Hospital/Dentistry'),
        ('S', 'Beauty Salon'),
    )
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_created = models.DateField(default=timezone.now)
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
    company_products = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

class StaffMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
