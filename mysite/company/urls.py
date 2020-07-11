from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.view_company, name='company-detail'),
    path('update/<int:pk>', views.update_company, name='company-update'),
    path('update/', views.update_company, name='company-update'),
    path('all/', views.CompanyList.as_view(), name='company-list'),
    path('my_companies/', views.view_my_companies, name='my-company-list'),
]
