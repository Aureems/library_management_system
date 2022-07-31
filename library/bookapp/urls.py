from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, AddBookView, AboutBookView, BookCatalogView, OrderBookView, \
    category_upload, author_upload, my_books, upload_file
from .views import AddCatView


urlpatterns = [
    path('category-upload/', category_upload, name='cat-upload'),
    # path('category-upload/', upload_file, name='cat-upload'),
    path('author-upload/', author_upload, name='auth-upload'),
    path('book-list/', BookListView.as_view(), name='books'),
    path('book-catalog/', BookCatalogView.as_view(), name='book-catalog'),
    path('book-order/', OrderBookView.as_view(), name='book-order'),
    path('my-books/', my_books, name='my-books'),
    path('add-book/', AddBookView.as_view(), name='add-book'),
    path('about-book/<pk>', AboutBookView.as_view(), name='about-book'),
    path('add-cat/', AddCatView.as_view(), name='add-cat'),
    # path('add-cat/', multiple_view, name='add-cat'),
]