from django.shortcuts import render
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