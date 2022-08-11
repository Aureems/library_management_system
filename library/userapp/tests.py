from django.test import TestCase, RequestFactory
from django.utils.timezone import now
from datetime import timedelta, datetime

from .models import User, Customer, Librarian
from .views import PasswordsChangeView, change_password, register_user
from .forms import PasswordChangeForm

class UserCreationTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        # customer
        self.test_user0 = User.objects.create(is_customer=True, is_librarian=False, email='email0@mail.com')
        # librarian
        self.test_user1 = User.objects.create(is_customer=False, is_librarian=True, email='email1@mail.com')
        # multiuser
        self.test_user2 = User.objects.create(is_customer=True, is_librarian=True, email='email2@mail.com')
        # superuser
        self.test_user3 = User.objects.create(is_customer=False, is_librarian=False, email='email3@mail.com')

        self.test_customer = Customer.objects.create(user=self.test_user0)
        self.test_librarian = Customer.objects.create(user=self.test_user1)
        self.test_multiuser = Customer.objects.create(user=self.test_user2)
        self.test_superuser = Customer.objects.create(user=self.test_user3)

    def test_user(self):
        self.assertEqual(self.test_customer.user.is_customer, True)
        self.assertEqual(self.test_customer.user.is_librarian, False)
        self.assertEqual(self.test_librarian.user.is_customer, False)
        self.assertEqual(self.test_librarian.user.is_librarian, True)
        self.assertEqual(self.test_multiuser.user.is_customer, True)
        self.assertEqual(self.test_multiuser.user.is_librarian, True)
        self.assertEqual(self.test_superuser.user.is_customer, False)
        self.assertEqual(self.test_superuser.user.is_librarian, False)


class DateTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = User.objects.create(is_customer=True, is_librarian=False, email='email0@mail.com')
        self.test_customer = Customer.objects.create(user=self.test_user, address='TestAddress',
                                                     birthday=(datetime.today()-timedelta(days=3)).strftime('%Y-%m-%d'))

    def test_date(self):
        self.assertEqual(self.test_customer.birthday, '2022-08-04')


class FormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(is_customer=True, username='testuser', email='email@email.com')
        self.user = User.objects.get(username='testuser')
        self.oldpassword = self.user.set_password('oldpassword')


    def test_change_password_form(self):

        # -------------------------------------unfilled form is not valid---------------------------
        form = PasswordChangeForm(user=self.user)
        self.assertFalse(form.is_valid())

        # -------------------------------old_password and new_password2 is required-------------------
        form = PasswordChangeForm(user=self.user, data={'new_password1': 'new1'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ['This field is required.'])
        self.assertEqual(form.errors['old_password'], ['This field is required.'])

        # ---------------------------------two passwords didn't match-----------------------------------------
        form = PasswordChangeForm(user=self.user, data={'old_password': 'old',
                                                        'new_password1': 'new1',
                                                        'new_password2': 'new2'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ['The two password fields didn’t match.'])

        # ------------------------------------incorrect old password------------------------------------------
        form = PasswordChangeForm(user=self.user, data={'old_password': 'old1',
                                                        'new_password1': 'new',
                                                        'new_password2': 'new'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'],
                         ['Your old password was entered incorrectly. Please enter it again.'])

        # ----------------------------------correct data and changed password (not working)---------------------
        # form = PasswordChangeForm(user=self.user, data={
        #                                                 'new_password1': 'new',
        #                                                 'new_password2': 'new'})
        # self.assertTrue(form.is_valid())
        # form.save()
        # self.assertEqual(self.user.old_password, 'new')
        # self.assertEqual(form.errors['old_password'],
        #                   ['Your old password was entered incorrectly. Please enter it again.'])
        # self.assertEquals(self.user.password, 'oldpassword')

