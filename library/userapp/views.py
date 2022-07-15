from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm


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
    return render(request, 'register.html', {'form': form})

class UserLogin(LoginView):
    template_name = 'login.html'

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, f'Your account is inactive')
                # return HttpResponse('Your account is inactive')
        else:
            messages.error(request, f'Your username or password is incorrect! Try again.')
            # return HttpResponse('Your username or password is incorrect! Try again.')
    return render(request, 'login.html', {})


def logout_user(request):
    return (request, 'logout.html')