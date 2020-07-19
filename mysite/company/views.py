from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from company.forms import CompanyForm
from company.models import Company


def update_company(request, company_id=None):
    if company_id:
        company_instance = Company.objects.get(pk=company_id)
    else:
        company_instance = Company()
    company_form = CompanyForm(instance=company_instance)

    if request.method == 'POST':
        if 'company_update' in request.POST:
            company_form = CompanyForm(request.POST)
            if company_form.is_valid():
                company_instance.name = company_form.cleaned_data['name']
                company_instance.description = company_form.cleaned_data['description']
                if company_id:
                    company_instance.manager = request.user
                    company_instance.date_created = timezone.now()
                company_instance.save()
            return redirect(reverse('company-detail', args=(company_instance.id,)))

        elif 'add_staff' in request.POST:
            user_to_add = request.POST['user_name']
            try:
                user = User.objects.get(username=user_to_add)
                company_instance.staff.add(user.profile)
            except User.DoesNotExist:
                messages.error(request,("error1"))

        elif 'remove_staff' in request.POST:
            username_to_remove = request.POST.get('user_to_remove', None)
            staffMember = company_instance.staff.remove(User.objects.get(username=username_to_remove).profile)

    return render(request, 'company/company_form.html',
                  {'company_form': company_form, 'staff_list': company_instance.staff.values('user__username')})


def view_company(request, pk):
    return render(request, 'company/company_detail.html', {'company_detail': Company.objects.get(pk=pk)})


def view_my_companies(request):
    return render(request, 'company/company_list.html',
                  {'company_list': Company.objects.all().filter(manager=request.user),
                   'edit': True, 'paginate': False, 'title': 'My Companies'})


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
