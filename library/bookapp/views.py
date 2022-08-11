import csv, io

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Book, Category, Author
from .forms import BookForm, AuthorForm, CategoryForm, CSVUploadForm, BookOrderForm
from django.db.models import Count
from django.db.models import Q


@login_required
@permission_required('userapp.User', raise_exception=True)
def category_upload(request):
    # template = 'bookapp/category-upload.html'
    template = 'bookapp/add-cat.html'

    if request.method == 'GET':
        return render(request, template)

    cat_file = request.FILES['category']

    if not cat_file.name.endswith('.csv'):
        return render(request, template, messages.error(request,'You can upload only CSV file'))

    try:
        data_set = cat_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=";"):
            _, created = Category.objects.update_or_create(
                category_name=column[0],
                subcategory_name=column[1],
            )
        context = {}
        return render(request, template, context, messages.success(request, 'File was uploaded successfully'))
    except Exception:
        return render(request, template, messages.error(request, 'File was not uploaded!'))


@login_required
@permission_required('userapp.User', raise_exception=True)
def author_upload(request):
    template = 'bookapp/author-upload.html'

    if request.method == 'GET':
        return render(request, template)

    auth_file = request.FILES['author']

    if not auth_file.name.endswith('.csv'):
        return render(request, template, messages.error(request,'You can upload only CSV file'))

    try:
        data_set = auth_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=";"):
            _, created = Author.objects.update_or_create(
                author_first_name=column[0],
                author_last_name=column[1],
                nationality=column[2],
                fiction_writer=column[3],
                nonfiction_writer=column[4],
            )
        context = {}
        return render(request, template, context, messages.success(request, 'File was uploaded successfully'))
    except Exception:
        return render(request, template, messages.error(request, 'File was not uploaded!'))


def upload_file(request):
    # template = 'bookapp/category-upload.html'
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # category_upload(request.FILE['file'])
            # return render(request, template)
            return redirect('books/category-upload')
        else:
            form = CSVUploadForm()
        return render(request, 'bookapp/category-upload.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(staff_member_required, name='dispatch')
class AddCatView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    login_url = 'login'
    template_name = 'bookapp/add-cat.html'
    success_url = reverse_lazy('categories')
    success_message = 'The category was added successfully!'


@method_decorator(staff_member_required, name='dispatch')
class AddAuthView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    login_url = 'login'
    template_name = 'bookapp/add-author.html'
    success_url = reverse_lazy('categories')
    success_message = 'Author was added successfully!'




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
    paginate_by = 8
    template_name = 'bookapp/book-list.html'
    success_url = '/'
    ordering = ['-available', '-date_created', 'title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cats'] = Book.objects.all().count()
        return context


class BookListByAuth(ListView):
    model = Book
    paginate_by = 8
    template_name = 'bookapp/book-list.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Book.objects.filter(author=self.kwargs.get('pk'))
        context['total_cats'] = Book.objects.filter(author=self.kwargs.get('pk')).count()
        return context



class OrderBookView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookOrderForm
    login_url = 'login'
    template_name = 'bookapp/order-book.html'
    success_url = reverse_lazy('my-books')
    success_message = 'Your ordered successfully!'
    # order = Order.objects.all()


class SubCategoryView(DetailView):
    model = Category
    template_name = 'bookapp/subcategories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcats'] = Category.objects.filter(category_name='Fiction')
        context['subcats2'] = Category.objects.filter(category_name='Nonfiction')
        return context


class BooksByCatView(ListView):
    model = Book
    template_name = 'bookapp/booksbycat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booksbycat'] = Book.objects.filter(category_id=self.kwargs['pk'])
        return context


class CategoryView(ListView):
    model = Category
    login_url = 'login'
    template_name = 'bookapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['total_cats'] = Category.objects.all().count()
        context['grouped'] = (Category.objects.values('category_name').annotate(dcount=Count('category_name')).order_by())
        context['fiction'] = Category.objects.filter(category_name='Fiction')
        context['nonfiction'] = Category.objects.filter(category_name='Nonfiction')
        return context