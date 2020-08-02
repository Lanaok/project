from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from profile.models import Manager
# Create your views here.
from company.models import Company
from company.models import Service
from company.models import StaffMember
from .forms import OrderForm
from .models import Order
from django.core.mail import send_mail
from company.views import staff_has_service
from profile.models import Profile
from django import forms


def MakeOrder(request, service_id):
    service_requested = Service.objects.get(pk=service_id)
    company = service_requested.company

    name = request.user.username
    staff_list = StaffMember.objects.filter(services=service_requested)

    order_instance = Order()
    order_form = OrderForm(instance=order_instance)

    if request.method == 'POST':

        time = request.POST['your-schedule']
        day = request.POST['your-time']
        message = request.POST['your-message']
        email_from = request.user.email  # ?
        manager = Manager.objects.get(company=company)
        message_for_send = message + ' ' + str(time) + ' ' + str(day) + ' ' + str(service_requested.name)
        manager_email = manager.profile.user.email
        send_mail(name, message_for_send, email_from, list(manager_email))
        return render(request, 'order/appointment.html')

    return render(request, 'order/make_order.html', {'username': name, 'staff': staff_list})
