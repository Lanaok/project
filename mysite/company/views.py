from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from company.forms import CompanyForm, StaffForm
from company.models import Company, StaffMember


def update_company(request, pk=None):
    if pk:
        company_instance = Company.objects.get(pk=pk)
    else:
        company_instance = Company()

    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_instance.name = company_form.cleaned_data['name']
            company_instance.description = company_form.cleaned_data['description']
            if pk:
                company_instance.manager = request.user
                company_instance.date_created = timezone.now()
            company_instance.save()

            return HttpResponseRedirect(reverse('company-detail', args=(company_instance.id,)))
    else:
        company_form = CompanyForm(instance=company_instance)

    return render(request, 'company/company_form.html', {'company_form': company_form})


def view_company(request, pk):
    return render(request, 'company/company_detail.html', {'company_detail': Company.objects.get(pk=pk)})


def view_my_companies(request):
    return render(request, 'company/company_list.html',
                  {'company_list': Company.objects.all().filter(manager=request.user),
                   'edit': True, 'paginate': False, 'title': 'My Companies'})


def add_staff_to_company(request):
    company_id = request.GET['company_id']
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        if staff_form.is_valid():
            if StaffMember.objects.filter(user=staff_form.cleaned_data['user_field'],
                                          company_id=company_id).count() > 0:
                staff_form.errors['user_field'] = ("already_member",)
                return render(request, 'company/company_add_member_form.html', {'staff_form': staff_form})
            else:
                StaffMember(user=staff_form.cleaned_data['user_field'], company_id=company_id).save()
            return HttpResponseRedirect(reverse('company-list'))
    else:
        staff_form = StaffForm(company_id=company_id)
    return render(request, 'company/company_add_member_form.html', {'staff_form': staff_form})


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
