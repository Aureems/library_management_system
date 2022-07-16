from django import forms
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import User
# from django.contrib.auth.models import User


class MyDatePickerInput(DatePickerInput):
    template_name = 'userapp/date-picker.html'


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(help_text=False, label='First Name')
    last_name = forms.CharField(help_text=False, label='Last Name')
    username = forms.CharField(help_text=False, label='Username')
    address = forms.CharField(help_text=False, label='Address', required=False)
    email = forms.EmailField(help_text=False, label='Email')
    birthday = forms.DateField(label='Date of Birth', input_formats=['%Y-%m/%d'], required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Confirm password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'address', 'email', 'birthday', 'password1', 'password2')
        widgets = {'birthday': MyDatePickerInput(format='%Y-%m-%d')}