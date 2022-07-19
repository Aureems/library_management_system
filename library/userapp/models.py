from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # is_customer = models.BooleanField(default=False)
    # is_librarian = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(null=True, max_length=50, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.email