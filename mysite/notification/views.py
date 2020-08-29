from django.shortcuts import redirect
# Create your views here.
from django.views.generic import ListView

from notification.models import Notification


class NotificationList(ListView):
    model = Notification
    template_name = 'notification/view_notifications.html'
    paginate_by = 6

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user.profile).order_by('-date_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Notifications"
        return context


def mark_all_as_read(request):
    Notification.objects.filter(read=False).update(read=True)
    return redirect('notifications-view')


def mark_as_read(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.read = True
    notification.save()
    return redirect(notification.link)
