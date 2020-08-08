from .models import Order
from django import forms
from crispy_forms.helper import FormHelper
from django.forms import TextInput, Textarea, Select, NumberInput, TimeInput, FileInput
from django.forms import ModelForm, TextInput, DateInput


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user_orders',  'staff_order', 'date_created', 'service_order']
        fields = ['order_time', 'order_day']
        widgets = {
            'order_time': DateInput(attrs={'class': 'form-control', 'type': 'time'}),
            'order_day': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
