from django.urls import path

from . import views
urlpatterns = [
    path('<int:pk>', views.view_company, name='company-detail'),
    path('update/<int:company_id>', views.update_company, name='company-update'),
    path('update/', views.update_company, name='company-update'),
    path('all/', views.CompanyList.as_view(), name='company-list'),
    path('my_companies/', views.view_my_companies, name='my-company-list'),
    # path('company/add_staff', views.add_staff_to_company, name='company-add-staff'),
]

