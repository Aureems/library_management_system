from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Book, Category
from .forms import BookForm, AuthorForm, CategoryForm


class AddBookView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    login_url = 'login'
    template_name = 'bookapp/add-book.html'
    success_url = reverse_lazy('books')
    success_message = 'The book was added successfully!'


class AboutBookView(DetailView):
    model = Book
    template_name = 'bookapp/about-book.html'
    book = Book.objects.all()


class AddCatView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    login_url = 'login'
    template_name = 'bookapp/add-cat.html'
    success_url = reverse_lazy('categories')
    success_message = 'The category was added successfully!'



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