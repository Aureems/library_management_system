from django.db import models
# from bookapp.models import Book
# from userapp.models import User
#
#
# class Order(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, on_delete = models.CASCADE)
#     isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
#     order_date = models.DateField()
#     due_to_date = models.DateField()
#
#     def __str__(self):
#         return f'{self.isbn}:{self.order_date}'
