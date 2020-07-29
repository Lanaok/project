from django import forms

from company.models import Company
from company.models import Service


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['date_created', 'manager', 'date_updated']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['company']
