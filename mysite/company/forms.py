from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import TextInput, Textarea, Select, NumberInput, TimeInput, FileInput

from company.models import Company
from company.models import Service
from company.models import Comment


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'company_type', 'working_hour_from', 'working_hour_to']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'company_type': Select(attrs={'class': 'form-control custom-select'}),
            'working_hour_from': TimeInput({'class': 'form-control', 'type': 'time'}),
            'working_hour_to': TimeInput({'class': 'form-control', 'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "company_form"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-5"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
