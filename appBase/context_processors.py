from notifications.models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')
        read_notifications = Notification.objects.filter(recipient=request.user, unread=False).order_by('-timestamp')[:10]  # Limita leídas
        return {
            'notifications_unread': unread_notifications,
            'notifications_read': read_notifications,
            'unread_count': unread_notifications.count()
        }
    return {
        'notifications_unread': [],
        'notifications_read': [],
        'unread_count': 0
    }