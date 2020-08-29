from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchResultList.as_view(), name='search'),
]
