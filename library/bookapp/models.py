from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(f"{self.category_id} - {self.category_name}")


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_first_name = models.CharField(max_length=100)
    author_last_name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.author_id} - {self.author_first_name} - {self.author_last_name}")


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=250)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    date_published = models.DateField()
    page_number = models.IntegerField(max_length=5)
    date_created = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='covers', default='default.png')

    def __str__(self):
        return str(f"{self.isbn} - {self.title}")