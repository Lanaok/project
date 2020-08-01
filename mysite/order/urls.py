from django.contrib import admin
from django.urls import path, include


from order import views
urlpatterns = [
    path('<int:company_id>/order/makeorder', views.MakeOrder, name='make_order')
]
