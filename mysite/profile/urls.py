from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.contact),
    path('update/', views.update_profile, name='profile-update'),
    path('', views.view_profile, name='profile-detail'),
]
