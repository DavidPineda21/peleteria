from . import views
from django.urls import path,include

urlpatterns = [


    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),



]