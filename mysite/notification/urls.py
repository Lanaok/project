from django.urls import path

from notification import views

urlpatterns = [
    path('', views.list_notifications, name='notifications-view'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark-all-as-read'),
]
