from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from bookapp.models import Book, Category, Author, MPTTCategory
from bookapp.forms import BookForm, AuthorForm, CategoryForm
from libapp.filters import CatFilter


class HomeView(ListView):
    model = Book
    login_url = 'login'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = Book.objects.all()
        return context


class CategoryView(ListView):
    model = Category
    login_url = 'login'
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['total_cats'] = Category.objects.all().count()
        context['grouped'] = (Category.objects.values('category_name').annotate(dcount=Count('category_name')).order_by())
        context['fiction'] = Category.objects.filter(category_name='Fiction')
        context['nonfiction'] = Category.objects.filter(category_name='Nonfiction')
        return context



class SubCategoryView(DetailView):
    model = Category
    template_name = 'subcategories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcats'] = Category.objects.filter(category_name='Fiction')
        context['subcats2'] = Category.objects.filter(category_name='Nonfiction')
        return context


class BooksByCatView(ListView):
    model = Book
    template_name = 'booksbycat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booksbycat'] = Book.objects.filter(category_id=self.kwargs['pk'])
        return context


class BooksByAuthView(ListView):
    pass


def about(request):
    return render(request, "about.html")


class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['booksbyauth'] = Book.objects.values('author_id').annotate(total=Count('isbn'))
        context['authbooks'] = Book.objects.values('author_id').annotate(total=Count('isbn')).order_by('-total')
        context['authorwithoutbook'] = Author.objects.exclude(author_id__in=Book.objects.values('author_id').distinct())
        return context


def categories(request):
    return render(request, "categories.html")


def contactus(request):
    return render(request, "contactus.html")


def faq(request):
    return render(request, "questions.html")


@login_required
@permission_required('userapp.User', raise_exception=True)
def managelib(request):
    return render(request, "managelib.html")
