from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from company.forms import CompanyForm
from company.models import Company


def update_company(request, pk):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_form.instance.manager = request.user
            company_instance = company_form.save()

            return redirect(f"/company/{company_instance.id}")
    else:
        if pk:
            instance = Company.objects.get(pk=pk)
        else:
            instance = Company()

        company_form = CompanyForm(instance=instance)

        return render(request, 'company/company_form.html', {'company_form': company_form})


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
