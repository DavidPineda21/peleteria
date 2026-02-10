from django.shortcuts import render
from notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# -----------------------------------------------------------------------------------------------------------------
@require_POST
def mark_notifications_as_read(request):
    # Marca todas las notificaciones no leídas como leídas
    Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
    return JsonResponse({'success': True})


# -----------------------------------------------------------------------------------------------------------------
@require_POST
def mark_notification_as_read(request):
    import json
    data = json.loads(request.body)
    notification_id = data.get('id')
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.unread = False
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
