from notification.models import Notification


def add_variable_to_context(request):
    if request.user.is_authenticated:
        return {
            "notification_count": Notification.objects.filter(read=False, receiver=request.user.profile).count()
        }
    return {"notification_count": 0}
