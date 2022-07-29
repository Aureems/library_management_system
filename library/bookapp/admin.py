# import mptt
# from django.db import models
# from mptt.fields import TreeForeignKey
from django.contrib import admin
from .models import Category, Author, Book

# TreeForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True).contribute_to_class(Category, 'subcategory')

admin.site.register(Category)
# mptt.register(Category)
admin.site.register(Author)
admin.site.register(Book)


