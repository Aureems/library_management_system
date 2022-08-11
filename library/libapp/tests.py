from django.test import TestCase, RequestFactory
from .models import Profile, Order, OrderItem, User, Book
from .views import HomeView


# Order_item creation test
class OrderItemTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_user', password='123456')
        test_items = Book.objects.create(isbn=123456, title='test_title', available=True, date_published='2022-08-05', page_number = 100)
        test_items2= Book.objects.create(isbn=1234567, title='test_title2', available=False, date_published='2022-08-05', page_number = 100)
        self.test_orderitem = OrderItem.objects.create(user=test_user, item=test_items, is_ordered=False, date_added='2022-08-08 17:51:27.222633 +00:00',
                                 date_ordered='2022-08-08 20:32:30.135604 +00:00')
        self.test_orderitem2 = OrderItem.objects.create(user=test_user, item=test_items2, date_added='2022-08-08 17:51:27.222633 +00:00',
                                                       date_ordered='2022-08-08 20:32:30.135604 +00:00')

    # Testing model string
    def test_model_str(self):
        self.assertEqual(str(self.test_orderitem), 'test_title')

    # Testing is_ordered item
    def test_orderitem_if_ordered_true(self):
        self.assertFalse(self.test_orderitem2.is_ordered)


# Order creation test
class OrderTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_username', password='123456')
        test_items = Book.objects.create(isbn=123456, title='test_title', available=True, date_published='2022-08-05',
                                         page_number=100)
        test_items2 = Book.objects.create(isbn=1234567, title='test_title2', available=False,
                                          date_published='2022-08-05', page_number=100)
        test_orderitem = OrderItem.objects.create(user=test_user, item=test_items, is_ordered=False,
                                                  date_added='2022-08-08 17:51:27.222633 +00:00',
                                 date_ordered='2022-08-08 20:32:30.135604 +00:00')
        test_orderitem2 = OrderItem.objects.create(user=test_user, item=test_items2, is_ordered=True,
                                                   date_added='2022-08-08 17:51:27.222633 +00:00',
                                 date_ordered='2022-08-08 20:32:30.135604 +00:00')
        self.test_order = Order.objects.create(ref_code='test_ref', user=test_user,
                                               is_ordered=False,
                                               date_ordered='2022-08-08 20:32:30.135604 +00:00',
                                               until_date='2022-08-09 20:32:30.135604 +00:00')
        self.test_order2 = Order.objects.create(ref_code='test_ref2', user=test_user,
                                                date_ordered='2022-08-08 20:32:30.135604 +00:00',
                                                until_date='2022-08-09 20:32:30.135604 +00:00')

        self.test_order.items.set = ([test_orderitem.pk, test_orderitem2.pk])

    # Testing model string
    def test_model_str(self):
        self.assertEqual(str(self.test_order), 'test_username:test_ref')


    def test_model(self):
        self.assertFalse(self.test_order.is_ordered)
        self.assertEqual(str(self.test_order2.user.username), 'test_username')


#HomeView request test
class MyProfileRequestTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_details(self):
        request = self.factory.get('/')
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
