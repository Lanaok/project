from django.db import models
from django.urls import reverse
from django.utils import timezone

from company.models import Company
from company.models import Service
from company.models import StaffMember
from profile.models import Profile


# Create your models here.
class Order(models.Model):
    class OrderState(models.TextChoices):
        requested = 'RE', 'requested'
        approved = 'AP', 'approved'
        denied = 'DE', 'denied'
        removed = 'REM', 'removed'

    user_orders = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    service_order = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    staff_order = models.ForeignKey(StaffMember, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    order_time = models.TimeField(default=timezone.now, null=False, blank=False)
    order_day = models.DateField(default=timezone.now, null=False, blank=False)
    order_state = models.CharField(choices=OrderState.choices, max_length=10)
    order_message = models.CharField(max_length=300)

    def __str__(self):
        return self.service_order.name

    def get_absolute_url(self):
        return reverse('order-view', args=[str(self.id)])

    @property
    def get_message(self):
        return ' service- ' + str(
            self.service_order.name) + ' on ' + str(self.order_day) + ' at ' + str(
            self.order_time) + ' with staff ' + str(self.staff_order)
