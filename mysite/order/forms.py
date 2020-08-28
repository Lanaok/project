from django import forms
from django.forms import DateInput

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user_orders',  'staff_order', 'date_created', 'service_order', 'order_state', 'order_message']
        fields = ['order_time', 'order_day']
        widgets = {
            'order_time': DateInput(attrs={'class': 'form-control', 'type': 'time'}),
            'order_day': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
