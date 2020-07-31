from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from company.forms import CompanyForm
from company.forms import ServiceForm
from company.models import Company, StaffMember
from company.models import Service
from profile import models
from profile.models import Manager, Profile


def edit_company(request, company_id=None):
    if company_id:
        company_instance = Company.objects.get(pk=company_id)
        if company_instance.manager != request.user.profile.manager:
            raise PermissionDenied
    else:
        company_instance = Company()
    company_form = CompanyForm(instance=company_instance)

    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_instance.name = company_form.cleaned_data['name']
            company_instance.description = company_form.cleaned_data['description']
            company_instance.company_type = company_form.cleaned_data['company_type']
            if company_id:
                company_instance.date_updated = timezone.now()
            else:
                try:
                    manager = Manager.objects.get(profile=request.user.profile)
                except Manager.DoesNotExist:
                    manager = Manager(profile=request.user.profile)
                    manager.save()

                company_instance.manager = manager
                company_instance.date_created = timezone.now()
            company_instance.save()
            return redirect(reverse('company-detail', args=(company_instance.id,)))

    return render(request, 'company/company/company_form.html',
                  {'company_form': company_form})


def view_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'company/company/company_detail.html',
                  {'company': company,
                   'show_edit_button': request.user.is_authenticated and company.manager.profile == request.user.profile})


def remove_company(request, company_id):
    Company.objects.get(pk=company_id).delete()
    return redirect('company-list')


def view_my_companies(request):
    return render(request, 'company/company/company_list.html',
                  {'company_list': Company.objects.all().filter(manager=request.user.profile.manager),
                   'paginate': False, 'title': 'My Companies'})


def staff_has_service(staff_instance, service_id):
    if staff_instance:
        return staff_instance.services.filter(pk=service_id).exists()
    return False


# TODO[IM]: add errors to form
def add_staff(request, company_id):
    company = Company(pk=company_id)
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
        except models.Profile.DoesNotExist:
            error_message = "could not find user"

    staff_service_list = list(
        map(lambda service: {'id': service.id, 'name': service.name}, company.service_set.all()))

    return render(request, 'company/staff/staff_edit.html',
                  {'service_list': staff_service_list, 'entered_username': entered_username,
                   'error_message': error_message})


def edit_staff(request, company_id, staff_id):
    staff_member = StaffMember.objects.get(pk=staff_id)
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
                  {'staff_member': staff_member, 'service_list': staff_service_list})


def remove_staff(request, company_id, staff_id):
    StaffMember.objects.get(pk=staff_id).delete()
    return redirect(reverse('staff-list', args=(company_id,)))


def list_staff(request, company_id):
    return render(request, 'company/staff/staff_list.html',
                  {'staff_list': StaffMember.objects.filter(company_id=company_id),
                   'company_id': company_id})


def edit_service(request, company_id, service_id=None):
    company = Company(pk=company_id)
    if service_id:
        service_instance = Service.objects.get(pk=service_id)
    else:
        service_instance = Service(company=company)
    service_form = ServiceForm(instance=service_instance)

    if request.method == 'POST':
        service_form = ServiceForm(request.POST, instance=service_instance)
        if service_form.is_valid():
            service_instance: Service = service_form.save(commit=False)
            service_instance.company = company
            service_instance.save()
        return redirect(reverse('service-list', args=(company_id,)))

    return render(request, 'company/services/service_form.html', {'service_form': service_form})


def remove_service(request, company_id, service_id):
    Service.objects.get(pk=service_id).delete()
    return redirect(reverse('service-list', args=(company_id,)))


def list_service(request, company_id):
    return render(request, 'company/services/service_list.html',
                  {'services': Service.objects.filter(company_id=company_id),
                   'company_id': company_id})


class CompanyList(ListView):
    model = Company
    template_name = "company/company/company_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.all().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Companies'
        return context
