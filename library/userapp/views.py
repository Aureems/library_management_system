from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm, PasswordChangingForm
from .models import User


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('home')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'userapp/change-password.html', {'form': form })


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, f'Account created for {username}! You are now able to login')
            return redirect('login')
    else:
         form = RegisterForm()
    return render(request, 'userapp/register.html', {'form': form})


class UserLogin(LoginView):
    template_name = 'userapp/login.html'


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                messages.error(request, f'Your account is inactive')
                # return HttpResponse('Your account is inactive')
        else:
            messages.error(request, f'Your username or password is incorrect! Try again.')
            # return HttpResponse('Your username or password is incorrect! Try again.')
    return render(request, 'login.html', {})


def logout_user(request):
    return (request, 'userapp/logout.html')


def view_profile(request):
    profile = User.objects.all()
    return render(request, 'userapp/profile.html')