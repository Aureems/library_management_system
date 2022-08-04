import random
import string

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.db.models import Q
from datetime import datetime

from .models import OrderItem, Order, Profile
from bookapp.models import Book, Category, Author, MPTTCategory
from bookapp.forms import BookForm, AuthorForm, CategoryForm
from libapp.filters import CatFilter


# REF CODE generating
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# profile View
def my_profile(request):
    return render(request, 'userapp/profile.html')

# def my_profile(request):
#     my_user_profile = Profile.objects.filter(user=request.user).first()
#     my_orders = Order.objects.filter(is_ordered=True, user=my_user_profile)
#     context = {
#         'my_orders': my_orders
#     }
#     return render(request, 'userapp/profile.html', context)

#
# class ProfileView(View):
#     model = Profile
#     template = 'userapp/profile.html'
#     login_url = 'login'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'libapp/cart/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return render('/')

# class OrderSummaryView(LoginRequiredMixin, View):
#     model = OrderItem
#     template = 'libapp/cart/cart.html'
#     login_url = 'login'


@login_required()
def add_to_cart(request, isbn):
    item = get_object_or_404(Book, isbn=isbn)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__isbn=item.isbn).exists():
            messages.warning(request, "You already own this book")
            return redirect('books')
        else:
            order.items.add(order_item)
            messages.info(request, "This book was added to your cart")
            return redirect('books')
    else:
        date_ordered = datetime.now()
        order = Order.objects.create(user=request.user, date_ordered=date_ordered)
        order.items.add(order_item)
        messages.info(request, "This book was added to your cart")
        return redirect('books')


@login_required()
def delete_from_cart(request, isbn):
    item = get_object_or_404(Book, isbn=isbn)
    order_qs = Order.objects.filter(user=request.user,is_ordered=False)
    # if order_qs.exists():
    order = order_qs[0]
    #     # check if the order item is in the order
    #     if order.items.filter(item__isbn=item.isbn).exists():
    order_item = OrderItem.objects.filter(item=item, user=request.user,is_ordered=False)[0]
    order.items.remove(order_item)
    messages.warning(request, "The book was removed")
    return redirect('cart')


@login_required()
def process_order(request, order_id):
    return redirect(reverse('update-records', kwargs={
        'order_id': order_id
    })
                    )

@login_required()
def update_transaction_records(request, order_id):
    # get the order being processed
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    # update placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    #update order items
    order_items.update(is_ordered=True, date_ordered=datetime.now())

    #Add items to user profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # get all the books from the items. Order model has ManyToMany field from Book model
    order_books = [item.book for item in order_items]
    # * - let's to add a list (order_books is a list) to user profile
    user_profile.books.add(*order_books)
    user_profile.save()



#
# class CartView(View, LoginRequiredMixin):
#     template_name = 'libapp/cart/cart.html'
#     login_url = 'login'
#
#     def get(self , request):
#         items = Cart.objects.all()
#         print(items)
#         return render(request , 'libapp/cart/cart.html' , {'items' : items} )


#
# def cart(request):
#     return render(request, 'libapp/cart/cart.html')
#
# def checkout(request):
#     return render(request, 'libapp/cart/checkout.html')


class HomeView(ListView):
    model = Book
    login_url = 'login'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = Book.objects.filter(category_id=40)
        context['math'] = Book.objects.filter(category_id=44)
        context['romance'] = Book.objects.filter(category_id=21)
        context['travel'] = Book.objects.filter(category_id=55)
        context['bookcount'] = Book.objects.prefetch_related('author').annotate(numb=Count('author'))
        context['authors'] = Author.objects.all().order_by('?')
        context['subcats'] = Category.objects.all()
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
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
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class SubCategoryView(DetailView):
    model = Category
    template_name = 'subcategories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcats'] = Category.objects.filter(category_name='Fiction')
        context['subcats2'] = Category.objects.filter(category_name='Nonfiction')
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class BooksByCatView(ListView):
    model = Book
    template_name = 'booksbycat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booksbycat'] = Book.objects.filter(category_id=self.kwargs['pk'])
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class AboutView(ListView):
    model = Book
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['booksbyauth'] = Book.objects.values('author_id').annotate(total=Count('isbn'))
        context['authbooks'] = Book.objects.values('author_id').annotate(total=Count('isbn')).order_by()
        context['authorwithoutbook'] = Author.objects.exclude(author_id__in=Book.objects.values('author_id').distinct())
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class ContactusView(ListView):
    model = Book
    template_name = 'contactus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


class FaqView(ListView):
    model = Book
    template_name = 'questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


@login_required
@permission_required('userapp.User', raise_exception=True)
def managelib(request):
    return render(request, "managelib.html")


class Search(ListView):
    model = Book
    template_name = 'search.html'
    context_object_name = 'results'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        search = Book.objects.all().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query))
        return search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', None)
        context['searchcount'] = Book.objects.all().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)).count()
        context['navsubcats'] = Category.objects.all()
        context['navbooks'] = Book.objects.all()
        return context


