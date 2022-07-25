from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView, UpdateView, DeleteView


def home(request):
    return render(request, "index.html")


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