from django.db import models


class Order(models.Model):
    pass


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100, Blank=True)

    def __str__(self):
        return str(f"{self.category_id} - {self.category_name}")


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_first_name = models.CharField(max_length=100)
    author_last_name = models.CharField(max_length=100)
    author_middle_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(f"{self.author_id} - {self.author_first_name}{' '+self.author_middle_name if not self.author_middle_name == '' else ''} {self.author_last_name}")


class Books(models.Model):
    isbn = models.CharField(primary_key=True, max_length=250)
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, null=True)
    description = models.CharField(max_length=10000)
    date_published = models.DateField()
    page_number = models.IntegerField(max_length=5)
    book_status = models.OneToOneField(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.isbn} - {self.title}")