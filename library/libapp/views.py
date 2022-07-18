from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, "home.html")


class BookOrderView(LoginRequiredMixin,CreateView):

    pass


def order_book(request):
    return render(request, "libapp/order.html")
