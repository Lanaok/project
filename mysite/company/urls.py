from django.urls import path

from . import views
from order.views import MakeOrder
urlpatterns = [
    path('<int:company_id>/view/', views.view_company, name='company-detail'),
    path('<int:company_id>/edit/', views.edit_company, name='company-update'),
    path('<int:company_id>/remove/', views.remove_company, name='company-remove'),
    path('add/', views.edit_company, name='company-update'),
    path('all/', views.CompanyList.as_view(), name='company-list'),
    path('my_companies/', views.view_my_companies, name='my-company-list'),

    path('<int:company_id>/staff/', views.list_staff, name='staff-list'),
    path('<int:company_id>/staff/add', views.add_staff, name='staff-add'),
    path('<int:company_id>/staff/<int:staff_id>/edit', views.edit_staff, name='staff-edit'),
    path('<int:company_id>/staff/<int:staff_id>/remove', views.remove_staff, name='staff-remove'),

    path('<int:company_id>/services/', views.list_service, name='service-list'),

    path('<int:company_id>/service/add', views.edit_service, name='service-add'),
    path('<int:company_id>/service/<int:service_id>', views.edit_service, name='service-view'), # todo change to view.
    path('<int:company_id>/service/<int:service_id>/edit/', views.edit_service, name='service-edit'),
    path('<int:company_id>/service/<int:service_id>/remove/', views.remove_service, name='service-remove'),
    path('<int:service_id>/order/', MakeOrder, name='make-order'),

]

