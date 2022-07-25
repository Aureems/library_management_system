from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from bookapp.models import Book
from bookapp.forms import BookForm, AuthorForm, CategoryForm


class HomeView(ListView):
    model = Book
    login_url = 'login'
    template_name = 'index.html'


def about(request):
    return render(request, "about.html")


def authors(request):
    return render(request, "authors.html")


def categories(request):
    return render(request, "categories.html")


def contactus(request):
    return render(request, "contactus.html")


def faq(request):
    return render(request, "faq.html")


@login_required
@permission_required('userapp.User', raise_exception=True)
def managelib(request):
    return render(request, "managelib.html")