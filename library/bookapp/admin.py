from django.contrib import admin
from .models import Category, Author, Book, MPTTCategory
from mptt.admin import MPTTModelAdmin

# TreeForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True).contribute_to_class(Category, 'subcategory')

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)

admin.site.register(MPTTCategory , MPTTModelAdmin)


