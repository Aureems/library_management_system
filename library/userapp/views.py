from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm



def register_user(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login')
        return redirect('home')
    else:
         reg_form = RegisterForm()
    return render(request, 'register.html', {'reg_form': reg_form })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is inactive')
        else:
            return HttpResponse('Your username or password is incorrect! Try again.')
    return render(request, 'login.html', {})


def logout_user(request):
    return (request, 'logout.html')