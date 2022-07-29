from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from bookapp.models import Book, Category
from bookapp.forms import BookForm, AuthorForm, CategoryForm



class HomeView(ListView):
    model = Book
    login_url = 'login'
    template_name = 'index.html'


class CategoryView(ListView):
    model = Category
    login_url = 'login'
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['total_cats'] = Category.objects.all().count()
        # context['total_books'] = Book.objects.filter(category=1).count()
        return context


class SubCategoryView(ListView):
    model = Category
    template_name = 'subcategories.html'

    # def get_context_data(self, **kwargs):
    #     catname = self.request.GET.get('name', None)
    #     if catname == None:
    #         context = super(SubCategoryView, self).get_context_data(**kwargs)
    #         context['subcat'] = Category.objects.filter(category_name='Fiction')
    #         return context
    #     else:
    #         context = super(SubCategoryView, self).get_context_data(**kwargs)
    #         context['subcat'] = Category.objects.filter(category_name='Nonfiction')
    #         return context

    def get_queryset(self):
        queryset = super(SubCategoryView, self).get_queryset().filter()
        query = self.request.GET.get("name", '')
        if query:
            queryset = Category.objects.filter(category_name__icontains=query)
        return queryset


def about(request):
    return render(request, "about.html")


def authors(request):
    return render(request, "authors.html")


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