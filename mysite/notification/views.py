from django.shortcuts import redirect
# Create your views here.
from django.views.generic import ListView

from notification.models import Notification


class NotificationList(ListView):
    model = Notification
    template_name = 'notification/view_notifications.html'
    paginate_by = 6

    def get_queryset(self):
        return Notification.objects.order_by('date_created')


def mark_all_as_read(request):
    Notification.objects.filter(read=False).update(read=True)
    return redirect('notifications-view')
