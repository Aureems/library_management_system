from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, AddBookView, AboutBookView, category_upload, author_upload
from .views import AddCatView


urlpatterns = [
    path('category-upload/', category_upload, name='cat-upload'),
    path('author-upload/', author_upload, name='auth-upload'),
    path('book-list/', BookListView.as_view(), name='books'),
    path('add-book/', AddBookView.as_view(), name='add-book'),
    path('about-book/<pk>', AboutBookView.as_view(), name='about-book'),
    path('add-cat/', AddCatView.as_view(), name='add-cat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)