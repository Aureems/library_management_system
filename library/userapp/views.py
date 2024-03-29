from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import CustomerRegisterForm, LibrarianRegisterForm, PasswordChangingForm, CustomerUpdateForm, UserUpdateForm
from .models import User, Customer, Librarian


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
        customer_form = CustomerRegisterForm(request.POST)
        librarian_form = LibrarianRegisterForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            username = customer_form.cleaned_data.get('username')
            messages.success(request, f'Customer account created for {username}! You are now able to login')
            return redirect('login')
        if librarian_form.is_valid():
            librarian_form.save()
            username = librarian_form.cleaned_data.get('username')
            messages.success(request, f'Librarian account created for {username}! You are now able to login')
            return redirect('login')
    else:
         customer_form = CustomerRegisterForm()
         librarian_form = LibrarianRegisterForm()
    return render(request, 'userapp/register.html', {'customer_form': customer_form, 'librarian_form': librarian_form})


class UserLogin(LoginView):
    template_name = 'userapp/login.html'
    # success_url = 'profile'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('managelib')
        else:
            return reverse('profile')



def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse('managelib'))
                elif user.is_customer:
                    login(request, user)
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse('lib-profile'))
            else:
                messages.error(request, f'Your account is inactive')
                # return HttpResponse('Your account is inactive')
        else:
            messages.error(request, f'Your username or password is incorrect! Try again.')
            # return HttpResponse('Your username or password is incorrect! Try again.')
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)


# @login_required()
# def edit_profile(request):
#     user = request.user
#     form_list = [{'form': UserUpdateForm, 'instance': user}]
#
#     if user.is_customer:
#         form_list.append({'form': CustomerUpdateForm, 'instance': user.customer})
#
#     forms = [x['form'](data=request.POST, instance=x['instance']) for x in form_list]
#     if request.method == 'POST':
#
#         if all([form.is_valid() for form in forms]):
#             for form in forms:
#                 form.save()
#             return redirect('profile')
#         else:
#             forms = [x['form'](instance=x['instance']) for x in form_list]
#     return render(request, 'userapp/profile-edit.html', {'forms': forms})

@login_required()
def edit_profile(request):
    user = request.user
    user_form = UserUpdateForm(request.POST, instance=user)

    if request.method == 'POST':

        if user_form.is_valid():
           user_form.save()
           messages.success(request, f'Your profile information has been updated.')
           return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, 'userapp/profile-edit.html', {'user_form':user_form})

@login_required()
def edit_customer_profile(request):
    user = request.user
    user_form = UserUpdateForm(request.POST, instance=user)
    cust_form = CustomerUpdateForm(request.POST, instance=user.customer)

    if request.method == 'POST':

        if user_form.is_valid() and cust_form.is_valid():
           cust_form.save()
           user_form.save()
           messages.success(request, f'Your profile information has been updated.')
           return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        cust_form = CustomerUpdateForm(instance=user.customer)

    return render(request, 'userapp/profile-edit.html', {'cust_form': cust_form, 'user_form':user_form})