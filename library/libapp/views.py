from django.shortcuts import render
from bookapp.models import Book
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def home(request):
    return render(request, "home.html")

class BookListView(ListView):
    model = Book
    # paginate_by = 4
    template_name = 'libapp/book-list.html'
    success_url = '/'