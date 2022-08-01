from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import User, Customer, Librarian
from django.db import transaction
# from django.contrib.auth.models import User


class ProfileForm():
    pass

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class MyDatePickerInput(DatePickerInput):
    template_name = 'userapp/date-picker.html'


class CustomerRegisterForm(UserCreationForm):
    first_name = forms.CharField(help_text=False, label='First Name')
    last_name = forms.CharField(help_text=False, label='Last Name')
    username = forms.CharField(help_text=False, label='Username')
    address = forms.CharField(help_text=False, label='Address', required=False)
    email = forms.EmailField(help_text=False, label='Email')
    birthday = forms.DateField(label='Date of Birth', widget=DatePickerInput(format='%Y-%m-%d'), input_formats=['%Y-%m-%d'], required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Confirm password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'address', 'email', 'birthday', 'password1', 'password2')
        widgets = {'birthday': MyDatePickerInput(format='%Y-%m-%d')}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.address = self.cleaned_data.get('address')
        customer.birthday = self.cleaned_data.get('birthday')
        customer.save()
        return user


class LibrarianRegisterForm(UserCreationForm):
    # first_name = forms.CharField(help_text=False, label='First Name')
    # last_name = forms.CharField(help_text=False, label='Last Name')
    username = forms.CharField(help_text=False, label='Username')
    email = forms.EmailField(help_text=False, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text=False, label='Confirm password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_librarian = True
        # user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.save()
        librarian = Librarian.objects.create(user=user)
        librarian.save()
        return user
