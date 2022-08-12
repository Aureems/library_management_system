from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput
from.models import Book, Author, Category

# from django.db.models import Count


class CSVUploadForm(forms.Form):
    file = forms.FileField()

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'

    def full_name(self):
        fullname = str(f"{self.firstname} - {self.lastname}")
        return fullname


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(max_length=100)
    subcategory_name = forms.CharField(max_length=100)

    class Meta:
        model = Category
        fields = '__all__'


class BookForm(forms.ModelForm):
    isbn = forms.CharField(label='ISBN', help_text=False)
    title = forms.CharField(label='Book title', help_text=False)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 200,
        'rows': 5,
        'style': 'width: 100%'
    }))
    date_published = forms.DateField(label='Date published', input_formats=['%Y-%m-%d'],
                                widget=DatePickerInput(format='%Y-%m-%d'))
    page_number = forms.IntegerField(label='Page number')
    photo = forms.ImageField(label='Book cover photo')

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'category', 'author', 'description', 'date_published', 'page_number', 'photo')


class BookOrderForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('isbn', 'title')
