from django import forms
from django.forms import DateInput

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_day', 'order_time']
        widgets = {
            'order_day': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'order_time': DateInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
