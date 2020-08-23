from django.urls import path

from order.views import order_view, order_change, order_remove

from . import views

urlpatterns = [
    # path('', views.contact),
    path('update/', views.update_profile, name='profile-update'),
    path('', views.view_profile, name='profile-detail'),
    path('orders/', views.view_orders, name='profile-orders'),
    path('orders/<int:order_id>/', order_view, name='order-view'),
    path('<int:order_id>/exchange/', order_change, name='order_change'),
    path('<int:order_id>/remove/', order_remove, name='order_remove'),
    path('orders/req/', views.order_requested, name='order_req'),
    path('orders/app/', views.order_approved, name='order_app'),
    path('orders/rem/', views.order_removed, name='order_rem'),
]
