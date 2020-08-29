from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms.utils import ErrorList
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from company.models import Service
from company.models import StaffMember
# Create your views here.
from notification.models import create_notification
from profile.models import Manager
from profile.models import Profile
from .forms import OrderForm
from .models import Order


def makeorder(request, service_id):
    service_requested = Service.objects.get(pk=service_id)
    company = service_requested.company

    name = request.user.username
    staff_list = StaffMember.objects.filter(services=service_requested)

    order_instance = Order()
    order_form = OrderForm(instance=order_instance)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        staff_member = request.POST['your-staff']
        time = request.POST['order_time']
        day = request.POST['order_day']
        message = request.POST['your-message']

        user = User.objects.get(username=staff_member)
        staff_profile = Profile.objects.get(user=user)
        orders = list(Order.objects.filter(staff_order=staff_profile.staffmember, order_day=day))
        if datetime.combine(datetime.strptime(day, '%Y-%m-%d').date(),
                            datetime.strptime(time, '%H:%M').time()) < datetime.today():
            errors = order_form.errors.setdefault('order_day', ErrorList())
            errors.append('date cannot be in past')
        elif not requested_hour_is_valid(orders, time):
            errors = order_form.errors.setdefault('order_time', ErrorList())
            errors.append('chosen time is booked')
        else:
            email_from = request.user.email  # ?
            manager = Manager.objects.get(company=company)
            message_for_send = message + ' service- ' + str(
                service_requested.name) + ' on ' + str(day) + ' at ' + str(time) + ' with staff ' + str(staff_member)
            manager_email = manager.profile.user.email
            send_mail(name, message_for_send, email_from, list(manager_email))
            order_instance.service_order = service_requested
            order_instance.staff_order = StaffMember.objects.get(profile=staff_profile)
            order_instance.user_orders = Profile.objects.get(user=request.user)
            order_instance.order_state = Order.OrderState.requested
            order_instance.order_day = day
            order_instance.order_time = time
            order_instance.order_message = message
            order_instance.save()
            create_notification("Order requested", order_instance.get_message, request.user.profile,
                                staff_profile.staffmember.company.manager.profile,
                                reverse('company-order', args=(company.id, "all")))
            return render(request, 'order/appointment.html', {'title': 'Appointment Requested'})

    return render(request, 'order/make_order.html', {'username': name, 'staff': staff_list, 'order_form': order_form,
                                                     'working_hour_from': company.working_hour_from,
                                                     'working_hour_to': company.working_hour_to,
                                                     'title': 'Book an Appointment'})


def order_view(request, order_id):
    order = Order.objects.get(pk=order_id)
    service = order.service_order
    company = service.company
    return render(request, 'order/order_detail.html',
                  {'order': order, 'userIsManager': company.manager.profile == request.user.profile,
                   'title': 'Order Details'})


def order_change(request, order_id):
    return render(request, 'order/order_change.html',
                  {'order': Order.objects.get(pk=order_id)})


def order_remove(request, order_id):
    user_order = Order.objects.get(pk=order_id)
    user_order.order_state = Order.OrderState.removed
    user_order.save()
    create_notification("Order removed", user_order.get_message, user_order.user_orders,
                        user_order.staff_order.company.manager.profile,
                        reverse('company-order', args=(user_order.staff_order.company.id, 'all')))
    return render(request, 'order/order_remove.html', {'title': 'Order Removed'})


def get_staff_schedule(request):
    if request.GET:
        staff = StaffMember.objects.get(pk=request.GET['staff_id'])
        date = datetime.strptime(request.GET['date'], '%Y-%m-%d')

        orders = list(Order.objects.filter(staff_order=staff, order_day=date))
        approved_intervals = []
        pending_intervals = []
        for order in orders:
            if order.order_state == Order.OrderState.approved:
                approved_intervals.append(
                    {'from': order.order_time, 'duration': order.service_order.duration.seconds / 3600})
            elif order.order_state == Order.OrderState.requested:
                pending_intervals.append(
                    {'from': order.order_time, 'duration': order.service_order.duration.seconds / 3600})

        return JsonResponse({'approved_intervals': approved_intervals, 'pending_intervals': pending_intervals})
    return None


def requested_hour_is_valid(orders, time):
    today = datetime.today()
    time = datetime.combine(today, datetime.strptime(time, '%H:%M').time())
    for order in orders:
        time_with_delta = time + order.service_order.duration
        order_time = datetime.combine(today, order.order_time)
        order_time_with_delta = order_time + order.service_order.duration
        if order_time <= time < order_time_with_delta or order_time <= time_with_delta < order_time_with_delta:
            return False
    return True
