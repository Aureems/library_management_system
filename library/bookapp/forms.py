from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from.models import Book, Author, Category


class AuthorForm(forms.ModelForm):
    firstname = forms.CharField(label='Author first name', help_text=False)
    lastname = forms.CharField(label='Author last name', help_text=False)

    class Meta:
        model = Author
        fields = '__all__'

    def full_name(self):
        fullname = str(f"{self.firstname} - {self.lastname}")
        return fullname


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(max_length=100)
    subcategory_name = forms.CharField(max_length=100)
    pass

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
    cover_photo = forms.ImageField(label='Book cover photo')

    class Meta:
        model = Book
        fields = ('isbn','title', 'category', 'author', 'description', 'date_published', 'page_number', 'cover_photo')

    # def clean(self):
    #     super(BookForm, self).clean()
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 5:
    #         self.errors['title'] = self.error_class([
    #             'Minimum 5 chars required'
    #         ])
    #     return self.cleaned_data