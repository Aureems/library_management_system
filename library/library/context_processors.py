from django.contrib.auth.models import User
from libapp.models import OrderItem, Order
from bookapp.models import Category, Book


def navbar_context(request):
    return {'ordercount': OrderItem.objects.filter(user=request.user.id, is_ordered=False).count(),
            'cartitems': OrderItem.objects.filter(user=request.user.id, is_ordered=False),
            'navsubcats': Category.objects.all(),
            'navbooks': Book.objects.all()
            }

