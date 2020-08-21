from django.db import models

# Create your models here.
from django.utils import timezone


class Notification(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=400)
    read = models.BooleanField(default=False, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def time_elapsed(self):
        time_diff = (timezone.now() - self.date_created).total_seconds()
        if time_diff <= 60:
            return str(int(time_diff)) + 's'
        elif 60 < time_diff <= 60 * 60:
            return str(int(time_diff / 60)) + 'm'
        elif time_diff / (60 * 60) <= 24:
            return str(int(time_diff / (60 * 60))) + 'h'
        else:
            return self.date_created.date()
