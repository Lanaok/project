from django import forms
from django.forms import TextInput, Textarea, Select, NumberInput, TimeInput, FileInput

from company.models import Company
from company.models import Service


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'company_type']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'company_type': Select(attrs={'class': 'form-control custom-select'}, )
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['company']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'duration': TimeInput(attrs={'class': 'form-control'}),
            'image': FileInput(attrs={'class': 'form-control'}),
        }
