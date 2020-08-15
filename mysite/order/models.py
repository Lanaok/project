from django.db import models
from django.urls import reverse

from company.models import Company
from company.models import Service
from company.models import StaffMember
from profile.models import Profile


# Create your models here.
class Order(models.Model):
    user_orders = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    service_order = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    staff_order = models.ForeignKey(StaffMember, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    order_time = models.DateField(null=True, blank=True)
    order_day = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.service_order.name

    def get_absolute_url(self):
        return reverse('order-view', args=[str(self.id)])
