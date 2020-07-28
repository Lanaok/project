from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from company.forms import CompanyForm
from company.forms import StaffForm
from company.forms import ServiceForm
from company.models import Company, StaffMember
from company.models import Service
from profile.models import Manager
import datetime


def update_company(request, company_id=None):
    if company_id:
        company_instance = Company.objects.get(pk=company_id)
        if company_instance.manager != request.user.profile.manager:
            raise PermissionDenied
    else:
        company_instance = Company()
    company_form = CompanyForm(instance=company_instance)

    if request.method == 'POST':
        if 'company_update' in request.POST:
            company_form = CompanyForm(request.POST)
            if company_form.is_valid():
                company_instance.name = company_form.cleaned_data['name']
                company_instance.description = company_form.cleaned_data['description']
                # company_instance.company_type = company_form.cleaned_data['company_type']
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
                staffers = StaffMember.objects.all().filter(company=company_instance)
            return redirect(reverse('company-detail', {'staff_member': staffers}))

    return render(request, 'company/company_form.html',
                  {'company_form': company_form})


def view_company(request, pk):
    company = Company.objects.get(pk=pk)
    staffers = StaffMember.objects.all().filter(company=company)
    if staffers is not None:
        return render(request, 'company/company_detail.html',
                      {'company_detail': company, 'show_edit_button': company.manager.profile == request.user.profile,
                       'staff_member': staffers})
    return render(request, 'company/company_detail.html',
                  {'company_detail': company, 'show_edit_button': company.manager.profile == request.user.profile})

def view_my_companies(request):
    return render(request, 'company/company_list.html',
                  {'company_list': Company.objects.all().filter(manager=request.user.profile.manager),
                   'edit': True, 'paginate': False, 'title': 'My Companies'})


def add_staff_to_company(request):
    comp_manager = Manager(profile=request.user.profile)
    company = Company(manager=comp_manager)
    staff_instance = StaffMember(company=company)
    staff_form = StaffForm(instance=staff_instance)
    if request.method == 'POST':
        if staff_form.is_valid():
            staff_instance.save()
            staff_form.save()
            staffers = StaffMember.objects.all().filter(company=company)
            return redirect(reverse('company-update', {'company_detail': company,
                                                       'show_edit_button': company.manager.profile == request.user.profile,
                                                       'staff_member': staffers}))

    return render(request, 'company/company_add_member_form.html', {'staff_form': staff_form})


def add_services_to_company(request):
    comp_manager = Manager(profile=request.user.profile)
    company = Company(manager=comp_manager)
    duration = datetime.timedelta(days=0)
    service_inst = Service(service_price=0, service_duration=duration)
    service_form = ServiceForm(instance=service_inst)
    if request.method == 'POST':
        if service_form.is_valid():
            service_inst.save()
            service_inst.save()
            company.save()
            list_services = Service.objects.all().filter(company=company)
            return render((reverse('company-update', {'list_of_services': list_services})))

    return render(request, 'company/company_add_service_form.html', {'service_form': service_form})


class CompanyList(ListView):
    model = Company
    template_name = "company/company_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.all().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Companies'
        return context


class StaffList(ListView):
    model = StaffMember
    template_name = "company/staff"
