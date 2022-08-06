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
from .forms import CheckoutForm
from bookapp.models import Book, Category, Author, MPTTCategory
from bookapp.forms import BookForm, AuthorForm, CategoryForm
from libapp.filters import CatFilter


# REF CODE generating
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))


# profile View
# def my_profile(request):
#     return render(request, 'userapp/profile.html')

def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user)[0]
    my_orders = Order.objects.filter(is_ordered=True, user=my_user_profile.user_id)
    my_not_returned_books = OrderItem.objects.filter(user=my_user_profile.user_id, is_ordered = True, date_returned__isnull=True)
    total_books = OrderItem.objects.filter(is_ordered=True, user=request.user).count()
    total_not_returned = OrderItem.objects.filter(date_returned__isnull=True,is_ordered=True, user=request.user).count()

    context = {
        'my_orders': my_orders,
        'my_not_returned_books': my_not_returned_books,
        'total_books': total_books,
        'total_not_returned': total_not_returned,
    }
    return render(request, 'userapp/profile.html', context)

#
# class ProfileView(View):
#     model = Profile
#     template = 'userapp/profile.html'
#     # login_url = 'login'


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {
                'object': order,
                'form': CheckoutForm
            }
            return render(self.request, 'libapp/cart/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect ('books')

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
            item.available = False
            item.save()
            messages.info(request, f'"{item.title}" was added to your cart')
            return redirect('books')
    else:
        date_ordered = datetime.now()
        order = Order.objects.create(user=request.user, date_ordered=date_ordered)
        order.items.add(order_item)
        item.available = False
        item.save()
        messages.info(request, f'"{item.title}" was added to your cart')
        return redirect('books')


@login_required()
def delete_from_cart(request, isbn):
    item = get_object_or_404(Book, isbn=isbn)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    order = order_qs[0]
    order_item = OrderItem.objects.filter(item=item, user=request.user, is_ordered=False)[0]
    order.items.remove(order_item)
    order_item.delete()
    item.available = True
    item.save()
    messages.warning(request, f'"{item.title}" book was removed from your cart')
    return redirect('cart')


@login_required()
def process_order(request, order_id):
    return redirect(reverse('checkout', kwargs={
        'order_id': order_id
    })
                    )

@login_required()
def confirm_order(request):
    # get the order being processed
    order_to_purchase_qs = Order.objects.filter(user=request.user, is_ordered=False)
    order_to_purchase = order_to_purchase_qs[0]

    # update placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.ref_code = create_ref_code()
    order_to_purchase.date_ordered = datetime.now()

    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    #update order items
    order_items.update(is_ordered=True, date_ordered=datetime.now())

    #Add items to user profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # get all the books from the items. Order model has ManyToMany field from Book model
    ordered_books = [order_item.item.pk for order_item in order_items]
    # * - lets to add a list (order_books is a list) to user profile
    user_profile.books.add(*ordered_books)
    user_profile.save()
    return redirect('profile')



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
        return context


class AboutView(ListView):
    model = Book
    template_name = 'about.html'


class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'
    paginate_by = 10
    queryset = Author.objects.all().order_by('author_last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booksbyauth'] = Book.objects.all()
        context['authbooks'] = Book.objects.values('author_id').annotate(total=Count('isbn')).order_by()
        context['authorwithoutbook'] = Author.objects.exclude(author_id__in=Book.objects.values('author_id').distinct())
        return context


class ContactusView(ListView):
    model = Book
    template_name = 'contactus.html'


class FaqView(ListView):
    model = Book
    template_name = 'questions.html'


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
            Q(author__author_last_name__icontains=query) |
            Q(author__author_first_name__icontains=query) |
            Q(description__icontains=query))
        return search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', None)
        context['searchcount'] = Book.objects.all().filter(
            Q(title__icontains=query) |
            Q(author__author_last_name__icontains=query) |
            Q(author__author_first_name__icontains=query) |
            Q(description__icontains=query)).count()
        return context


