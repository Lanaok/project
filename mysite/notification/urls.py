from django.urls import path

from notification import views

urlpatterns = [
    path('', views.NotificationList.as_view(), name='notifications-view'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark-all-as-read'),
]
