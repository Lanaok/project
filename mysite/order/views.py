from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
# Create your views here.
from company.models import Company
from company.models import Service
from company.models import StaffMember
from .forms import OrderForm
from .models import Order

def MakeOrder(request, company_id):
    company = Company(pk=company_id)
    name = request.user.username
    company_service_list = Service.objects.filter(company_id=company_id)
    company_staff_list = StaffMember.objects.filter(company_id=company_id)
    order_instance = Order()
    #order_instance.service_order = company_service_list
    #order_instance.staff_order = company_staff_list
    order_form = OrderForm(instance=order_instance)
    if request.method == 'POST':
        pass
    # order_service_list = list(
    #    map(lambda service: {'id': service.id, 'name': service.name}, company.service_set.all()))
    return render(request, 'order/make_order.html', {'username': name, 'service_list': company_service_list,
                                                     'staff_list': company_staff_list, 'order_form': order_form})
