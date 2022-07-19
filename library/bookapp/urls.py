from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, add_book


urlpatterns = [
    path('book-list/', BookListView.as_view(), name='books'),
    path('add-book/', add_book, name='add-book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)