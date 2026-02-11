from . import views
from django.urls import path,include

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('captcha/', include('captcha.urls')),
    path('change_password/', views.change_password, name='change_password'),


    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),

    path('restringido/', views.accesoRestringido, name='accesoRestringido'),



]