from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)

    def __str__(self):
        return self.email

    # USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS=[]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.email

    # USERNAME_FIELD = 'email'


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email

    # USERNAME_FIELD = 'email'
