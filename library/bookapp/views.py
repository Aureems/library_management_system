from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book
from .forms import BookForm, AuthorForm, CategoryForm


def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        author_form = AuthorForm(request.POST)
        category_form = CategoryForm(request.POST)
        if book_form.is_valid and author_form.is_valid and category_form.is_valid:
            book_form.save()
            author_form.save()
            category_form.save()
            messages.success(request, f'Data was saved')
        else:
            messages.error(request, f'Not all fields was filled')
    else:
        book_form = BookForm()
        author_form = AuthorForm()
        category_form = CategoryForm
    context = {
        'book_form': book_form,
        'author_form': author_form,
        'category_form': category_form,
    }
    return render(request, 'bookapp/add-book.html', context=context)



class BookListView(ListView):
    model = Book
    # paginate_by = 4
    template_name = 'bookapp/book-list.html'
    success_url = '/'