from django.db import models
from company.models import Company
from company.models import Service
from company.models import StaffMember
from profile.models import Profile
# Create your models here.
class Order(models.Model):
    user_orders = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    company_orders = models.ManyToManyField(Company)
    service_order = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    staff_order = models.ForeignKey(StaffMember, null=True, on_delete=models.SET_NULL)
