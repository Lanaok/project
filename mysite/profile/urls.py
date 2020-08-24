from django.urls import path

from order.views import order_view, order_change, order_remove
from . import views

urlpatterns = [
    # path('', views.contact),
    path('update/', views.update_profile, name='profile-update'),
    path('', views.view_profile, name='profile-detail'),
    path('orders/<str:filter>/', views.ProfileOrderList.as_view(), name='profile-orders'),
    path('orders/<int:order_id>/', order_view, name='order-view'),
    path('<int:order_id>/exchange/', order_change, name='order_change'),
    path('<int:order_id>/remove/', order_remove, name='order_remove'),
]
