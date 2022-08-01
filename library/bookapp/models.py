from django.db import models
from django.core.validators import MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from userapp.models import User

from django.dispatch import receiver


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True)
    subcategory_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # upload = models.FileField(upload_to='csv_uploads', blank=True, null=True)


    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('category_name', 'subcategory_name', )

    def __str__(self):
        return str(f"{self.subcategory_name}")


class MPTTCategory(MPTTModel):
    categ_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['categ_name']

    class Meta:
        verbose_name_plural = 'MPTTCategories'

    def __str__(self):
        return str(f"{self.categ_name}")


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_first_name = models.CharField(max_length=100)
    author_last_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    fiction_writer = models.BooleanField(default=False, blank=True, null=True)
    nonfiction_writer = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('author_last_name','author_first_name',)

    def __str__(self):
        return str(f"{self.author_first_name} {self.author_last_name}")


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13, unique=True)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=9999)
    date_published = models.DateField()
    page_number = models.IntegerField(validators=[MaxValueValidator(9999)])
    date_created = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='covers', default='covers/default.jpg')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateField()
    due_to_date = models.DateField()


    def __str__(self):
        return {self.order_id}