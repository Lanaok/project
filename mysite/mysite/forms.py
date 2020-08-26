from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)
        self.fields.move_to_end('last_name', last=False)
        self.fields.move_to_end('first_name', last=False)

    def save(self, request):
        user: User = super(MyCustomSignupForm, self).save(request)
        first_name = self.cleaned_data.pop('first_name')
        last_name = self.cleaned_data.pop('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user
