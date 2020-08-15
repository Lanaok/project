from notification.models import Notification


def add_variable_to_context(request):
    return {
        "notification_count": Notification.objects.filter(read=False).count()
    }
