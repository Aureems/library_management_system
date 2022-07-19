from django.shortcuts import render
from .models import Book
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class BookListView(ListView):
    model = Book
    # paginate_by = 4
    template_name = 'bookapp/book-list.html'
    success_url = '/'