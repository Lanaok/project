from django.urls import path

from . import views
urlpatterns = [
    path('<int:company_id>/view/', views.view_company, name='company-detail'),
    path('<int:company_id>/edit/', views.update_company, name='company-update'),
    path('add/', views.update_company, name='company-update'),
    path('all/', views.CompanyList.as_view(), name='company-list'),
    path('my_companies/', views.view_my_companies, name='my-company-list'),

    path('<int:company_id>/staff/', views.staff_list, name='staff-list'),
    path('<int:company_id>/staff/add', views.staff_add, name='staff-add'),
    path('<int:company_id>/staff/<int:staff_id>/edit', views.staff_edit, name='staff-edit'),
    path('<int:company_id>/staff/<int:staff_id>/remove', views.staff_remove, name='staff-remove'),

    path('<int:company_id>/services/', views.service_list, name='service-list'),
    path('<int:company_id>/service/add', views.service_add, name='service-add'),
    path('<int:company_id>/service/<int:service_id>', views.service_add, name='service-view'), # todo change to view.
    path('<int:company_id>/service/<int:service_id>/edit/', views.service_add, name='service-edit'),
    path('<int:company_id>/service/<int:service_id>/remove/', views.service_remove, name='service-remove'),

]

