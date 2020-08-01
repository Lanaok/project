from .models import Order
from django import forms
from django.forms import TextInput, Textarea, Select, NumberInput, TimeInput, FileInput

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude =['user_orders', 'company_orders', 'staff_order']


