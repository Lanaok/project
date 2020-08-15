from django.shortcuts import render, redirect

# Create your views here.
from notification.models import Notification


def list_notifications(request):
    return render(request, 'notification/view_notifications.html', {"notifications": Notification.objects.all()})


def mark_all_as_read(request):
    Notification.objects.filter(read=False).update(read=True)
    return redirect('notifications-view')
