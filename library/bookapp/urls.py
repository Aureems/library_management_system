from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, AddBookView, AboutBookView, OrderBookView, \
    category_upload, author_upload, upload_file, BookListByAuth
from .views import AddCatView, CategoryView, SubCategoryView,\
    BooksByCatView, AddAuthView


urlpatterns = [
    path('category-upload/', category_upload, name='cat-upload'),
    # path('category-upload/', upload_file, name='cat-upload'),
    path('author-upload/', author_upload, name='auth-upload'),
    path('book-list/', BookListView.as_view(), name='books'),
    path('book-list/?q=<pk>', BookListByAuth.as_view(), name='books-byauth'),
    path('book-order/', OrderBookView.as_view(), name='book-order'),
    path('add-book/', AddBookView.as_view(), name='add-book'),
    path('about-book/<pk>', AboutBookView.as_view(), name='about-book'),
    path('add-cat/', AddCatView.as_view(), name='add-cat'),
    path('add-auth/', AddAuthView.as_view(), name='add-auth'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/<pk>', SubCategoryView.as_view(), name='subcat-list'),
    path('books-by-subcat/<str:pk>', BooksByCatView.as_view(), name='books-by-cat'),
    # path('add-cat/', multiple_view, name='add-cat'),
]