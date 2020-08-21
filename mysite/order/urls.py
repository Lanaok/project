from django.urls import path

from order import views

urlpatterns = [
    path('get_staff_schedule/', views.get_staff_schedule, name='get-staff-schedule'),
]
