"""
Context processors for the finance app.
These run on every request and inject variables into all templates.
"""
from .models import Notification


def unread_notifications(request):
    """Inject unread notification count into every template."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}
