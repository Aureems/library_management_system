import django_filters
from bookapp.models import Category


class CatFilter(django_filters.FilterSet):

    class Meta:
        model = Category
        fields = ('category_name', 'subcategory_name')