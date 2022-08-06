from django.db import models
from bookapp.models import Book
from userapp.models import User
from django.db.models.signals import post_save
from datetime import datetime, timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.user.username


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=User)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    is_ordered = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.item.title


class Order(models.Model):
    ref_code = models.CharField(max_length=9, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    is_ordered = models.BooleanField(default=False, null=True, blank=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    until_date = models.DateTimeField(null=True, blank=True)

    def get_cart_items(self):
        return self.items.all()

    def __str__(self):
        return f'{self.user}:{self.ref_code}'

