from models import Book
from django import forms


class AddBook(forms.ModelForm):
    isbn = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    category = forms.CharField(max_length=250)
    subcategory = forms.CharField(max_length=250)
    author = forms.CharField(max_length=250)
    description = forms.Textarea()
    date_published = forms.DateField()
    page_number = forms.IntegerField(max_value=6)
    photo = forms.ImageField(upload_to='covers', default='default.png')

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'category', 'subcategory', 'author', 'description',  'date_published',
                  'page_number', 'photo', )

# class AddAuthor(forms.ModelForm):
#     first_name = forms.CharField()
#
# class AddCategory(forms.ModelForm):
#
#
