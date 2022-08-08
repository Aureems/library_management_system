from django import forms
from .models import Order
from datetime import datetime, timedelta
from bootstrap_datepicker_plus.widgets import DatePickerInput


class CheckoutForm(forms.ModelForm):

    until_date = forms.DateTimeField(label='Order until',
                                     input_formats=['%Y-%m-%d %H:%M'],
                                     widget=DatePickerInput(format='%Y-%m-%d %H:%M'),
                                     required=True)

    class Meta:
        model = Order
        fields = '__all__'




