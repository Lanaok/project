from django import forms

from company.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['date_created']


# class StaffForm(forms.Form):
#     user_field = forms.ModelChoiceField(queryset=User.objects.all(), label='User:', empty_label='None')
#
#     def __init__(self, *args, **kwargs):
#         company_id = kwargs.pop('company_id', None)
#         super(StaffForm, self).__init__(*args, **kwargs)
#         if company_id:
#             try:
#                 self.fields['user_field'].queryset = User.objects.exclude(
#                     id__in=StaffMember.objects.filter(company_id=company_id).values('user_id'))
#             except StaffMember.DoesNotExist:
#                 pass
