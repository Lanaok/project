from .models import Order
from django import forms
from crispy_forms.helper import FormHelper
from django.forms import TextInput, Textarea, Select, NumberInput, TimeInput, FileInput


class OrderForm(forms.ModelForm):
    helper = FormHelper()
    helper.Form_show_labels = False

    class Meta:
        model = Order
        exclude = ['user_orders', 'company_orders', 'staff_order']
