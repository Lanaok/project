from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views.generic import ListView

from company.forms import CompanyForm, CommentForm
from company.forms import ServiceForm
from company.models import Company, StaffMember, Comment
from company.models import Service
from notification.models import create_notification
from order.models import Order
from profile import models
from profile.models import Manager, Profile


@login_required
def edit_company(request, company_id=None):
    if company_id:
        company_instance = Company.objects.get(pk=company_id)
        check_manager_permission(company_instance.manager, request.user)
    else:
        company_instance = Company()
    company_form = CompanyForm(instance=company_instance)

    if request.method == 'POST':
        company_form = CompanyForm(request.POST, instance=company_instance, files=request.FILES)
        if company_form.is_valid():
            if not company_id:
                try:
                    manager = Manager.objects.get(profile=request.user.profile)
                except Manager.DoesNotExist:
                    manager = Manager(profile=request.user.profile)
                    manager.save()
                company_instance = company_form.save(commit=False)
                company_instance.manager = manager
            company_instance.save()
            return redirect(reverse('company-detail', args=(company_instance.id,)))

    return render(request, 'company/company/company_form.html',
                  {'company_form': company_form,
                   'title': 'Update Company'})


def view_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'company/company/company_detail.html',
                  {'company': company,
                   'show_edit_button': request.user.is_authenticated and company.manager.profile == request.user.profile,
                   'title': 'Company Details'})


@login_required
def remove_company(request, company_id):
    company_instance = Company.objects.get(pk=company_id)
    check_manager_permission(company_instance, request.user)
    Company.objects.get(pk=company_id).delete()
    return redirect('company-list')


@login_required
def view_my_companies(request):
    if Manager.objects.filter(profile=request.user.profile).exists():
        company_manager = request.user.profile.manager
        return render(request, 'company/company/company_list.html',
                      {'company_list': Company.objects.all().filter(manager=company_manager),
                       'paginate': False, 'title': 'My Companies'})
    return render(request, 'company/company/company_list.html', {'title': 'All Companies'})


def staff_has_service(staff_instance, service_id):
    if staff_instance:
        return staff_instance.services.filter(pk=service_id).exists()
    return False


# TODO[IM]: add errors to form
@login_required
def add_staff(request, company_id):
    company = Company.objects.get(pk=company_id)
    check_manager_permission(company.manager, request.user)
    entered_username = None
    error_message = None
    if request.method == 'POST':
        try:
            entered_username = request.POST['username']
            profile = Profile.objects.filter(user__username=entered_username).get()
            if StaffMember.objects.filter(profile=profile, company=company).exists():
                error_message = "user is already a member"
            else:
                staff_service_list = request.POST.getlist('checked_services')
                staff_member = StaffMember(profile=profile, company=company)
                staff_member.save()
                for checked_service_id in staff_service_list:
                    staff_member.services.add(checked_service_id)
                return redirect(reverse('staff-list', args=(staff_member.company_id,)))
        except models.Profile.DoesNotExist:
            error_message = "could not find user"

    staff_service_list = list(
        map(lambda service: {'id': service.id, 'name': service.name}, company.service_set.all()))

    return render(request, 'company/staff/staff_edit.html',
                  {'service_list': staff_service_list, 'entered_username': entered_username,
                   'error_message': error_message,
                   'title': 'Add Staff'})


@login_required
def edit_staff(request, staff_id):
    staff_member = StaffMember.objects.get(pk=staff_id)
    check_manager_permission(staff_member.company.manager, request.user)
    if request.method == 'POST':
        new_staff_service_list = request.POST.getlist('checked_services')
        staff_member.services.clear()
        for checked_service_id in new_staff_service_list:
            staff_member.services.add(checked_service_id)
        staff_member.save()
        return redirect(reverse('staff-list', args=(staff_member.company.id,)))

    company = staff_member.company
    staff_service_list = list(
        map(lambda service: {'id': service.id, 'name': service.name,
                             'is_checked': staff_has_service(staff_member, service.id)}, company.service_set.all()))
    return render(request, 'company/staff/staff_edit.html',
                  {'staff_member': staff_member, 'service_list': staff_service_list, 'title': 'Update Staff'})


def view_staff(request, staff_id):
    return render(request, 'company/staff/staff_detail.html',
                  {'staff_member': StaffMember.objects.get(pk=staff_id), 'title': 'Staff Details'})


@login_required
def remove_staff(request, staff_id):
    staff_member = StaffMember.objects.get(pk=staff_id)
    check_manager_permission(staff_member.company.manager, request.user)
    company_id = staff_member.company_id
    staff_member.delete()
    return redirect(reverse('staff-list', args=(company_id,)))


class StaffList(ListView):
    model = StaffMember
    template_name = "company/staff/staff_list.html"
    paginate_by = 6

    def get_queryset(self):
        return StaffMember.objects.filter(company_id=self.kwargs['company_id']).order_by('date_joined')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=self.kwargs['company_id'])
        context['title'] = 'Staff List'
        return context


@login_required
def edit_service(request, company_id, service_id=None):
    company = Company(pk=company_id)
    check_manager_permission(company.manager, request.user)
    if service_id:
        service_instance = Service.objects.get(pk=service_id)
    else:
        service_instance = Service(company=company)
    service_form = ServiceForm(instance=service_instance)

    if request.method == 'POST':
        service_form = ServiceForm(request.POST, instance=service_instance, files=request.FILES)
        if service_form.is_valid():
            service_instance: Service = service_form.save(commit=False)
            service_instance.company = company
            service_instance.save()
        return redirect(reverse('service-list', args=(company_id,)))

    return render(request, 'company/services/service_form.html',
                  {'service_form': service_form, 'title': 'Update Service'})


@login_required
def remove_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    check_manager_permission(service.company.manager, request.user)
    company_id = service.company_id
    service.delete()
    return redirect(reverse('service-list', args=(company_id,)))


class ServiceList(ListView):
    model = Service
    template_name = "company/services/service_list.html"
    paginate_by = 6

    def get_queryset(self):
        return Service.objects.filter(company_id=self.kwargs['company_id']).order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=self.kwargs['company_id'])
        context['title'] = 'Service List'
        return context


def view_service(request, service_id):
    return render(request, 'company/services/service_detail.html',
                  {'service': Service.objects.get(pk=service_id), 'title': 'Service Details'})


class CompanyOrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = "company/company/company_orders.html"
    paginate_by = 9

    def get_queryset(self):
        check_manager_permission(Company.objects.get(pk=self.kwargs['company_id']).manager, self.request.user)
        if self.kwargs['filter'] != 'all':
            return Order.objects.filter(service_order__company_id=self.kwargs['company_id'],
                                        order_state=self.kwargs['filter']).order_by('-date_created')
        else:
            return Order.objects.filter(service_order__company_id=self.kwargs['company_id']).order_by('-date_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_states'] = Order.OrderState
        context['company_id'] = self.kwargs['company_id']
        context['active_tab'] = self.kwargs['filter'] + "-tab"
        context['title'] = 'Company Orders'
        return context


@login_required
def update_company_orders(request, company_id):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_obj = Order.objects.get(pk=order_id)
        check_manager_permission(order_obj.service_order.company.manager, request.user)
        if 'but1' in request.POST:
            order_obj.order_state = Order.OrderState.approved
            order_obj.save()
            create_notification("Order approved", order_obj.get_message, order_obj.staff_order.company.manager.profile,
                                order_obj.user_orders,
                                reverse('profile-orders', args=('all',)))
        elif 'but2' in request.POST:
            order_obj.order_state = Order.OrderState.denied
            order_obj.save()
            create_notification("Order denied", order_obj.get_message, order_obj.staff_order.company.manager.profile,
                                order_obj.user_orders,
                                reverse('profile-orders', args=('all',)))

    return redirect(request.META.get('HTTP_REFERER'))


class CompanyList(ListView):
    model = Company
    template_name = "company/company/company_list.html"
    paginate_by = 6

    def get_queryset(self):
        return Company.objects.all().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Companies'
        return context


@login_required
def add_comment(request, company_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.company_id = company_id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table

    comments_list = Comment.objects.all().filter(company=Company.objects.get(pk=company_id))
    return render(request, "company/company/review_message.html", {'comments_list': comments_list})


def check_manager_permission(company_manager, user):
    try:
        if company_manager != user.profile.manager:
            raise PermissionDenied
    except Exception:
        raise PermissionDenied
