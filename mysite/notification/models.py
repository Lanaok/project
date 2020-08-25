from django.db import models
# Create your models here.
from django.utils import timezone

from profile.models import Profile


class Notification(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=400)
    read = models.BooleanField(default=False, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, related_name="receiver")
    link = models.CharField(max_length=200, blank=False, null=False)

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


def create_notification(title: str, description: str, sender: Profile, receiver: Profile, link: str):
    notification = Notification(title=title, description=description, sender=sender, receiver=receiver, link=link)
    notification.save()
