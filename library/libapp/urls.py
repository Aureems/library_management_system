"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, about, AuthorListView, contactus, faq, managelib, CategoryView, SubCategoryView,\
    BooksByCatView, Search, my_profile, OrderSummaryView, add_to_cart, process_order, update_transaction_records, \
    delete_from_cart



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/<pk>', SubCategoryView.as_view(), name='subcat-list'),
    path('books-by-subcat/<str:pk>', BooksByCatView.as_view(), name='books-by-cat'),
    path('search/', Search.as_view(), name='search'),
    path('contactus/', contactus, name='contactus'),
    path('faq/', faq, name='faq'),
    path('managelib/',  managelib, name='managelib'),
    path('cart/', OrderSummaryView.as_view(), name='cart'),
    path('cart/add-to-cart/<isbn>', add_to_cart, name='add-to-cart'),
    path('cart/delete-from-cart/<isbn>', delete_from_cart, name='delete-from-cart'),
    # path('checkout/', checkout, name='checkout'),
    # path('process-order/<pk>', process_order, name='process-order'),
    path('update-transaction/<pk>', update_transaction_records, name='update-transaction'),
    path('profile/', my_profile , name='profile'),
]
