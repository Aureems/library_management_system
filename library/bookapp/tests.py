from django.test import TestCase, RequestFactory
from .models import Author, Category, Book
from .views import category_upload, AboutBookView

# Author creation test
class AuthorTestCase(TestCase):
    def create_author(self, author_first_name='test_name', author_last_name='test_last_name',
                      nationality='American', fiction_writer=False):
        return Author.objects.create(author_first_name='test_name', author_last_name='test_last_name',
                                    nationality='American', fiction_writer=False)

    def test_author_nationality(self):
        author = self.create_author()
        self.assertEqual(author.nationality, 'American')

# Category creation test
class CategoryTestCase(TestCase):
    def create_category(self, category_name='test_category', subcategory_name='test_subcategory'):
        return Category.objects.create(category_name='test_category', subcategory_name='test_subcategory')

    def test_subcategory_name(self):
        category = self.create_category()
        self.assertEqual(category.subcategory_name, 'test_subcategory')

# Book creation test
class BookModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_author1=Author.objects.create(author_first_name='test_name1',author_last_name='test_last_name1')
        cls.test_category1=Category.objects.create(category_name='test_category1',subcategory_name='test_subcategory1')
        cls.test_author2 = Author.objects.create(author_first_name='test_name2', author_last_name='test_last_name2')
        cls.test_category2 = Category.objects.create(category_name='test_category2', subcategory_name='test_subcategory2')
        cls.book1 = Book.objects.create(isbn='123',
                                        title='test_book1',
                                        category=cls.test_category1,
                                        author=cls.test_author1,
                                        description='This is test',
                                        date_published='2021-01-01',
                                        page_number=150,
                                        available=True)
        cls.book2 = Book.objects.create(isbn='456',
                                        title='test_book2',
                                        category=cls.test_category2,
                                        author=cls.test_author2,
                                        description='This is test2',
                                        date_published='2022-01-01',
                                        page_number=200,
                                        available=False)

    def test_book(self):
        self.assertEqual(self.book1.author.author_first_name, 'test_name1')
        self.assertEqual(self.book2.category.subcategory_name, 'test_subcategory2')
        self.assertEqual(self.book1.author.author_last_name, 'test_last_name1')
        self.assertEqual(self.book1.available, True)


#category_upload request test
class CatUploadRequestTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_details(self):
        request = self.factory.get('/books/category-upload')
        response = category_upload(request)
        self.assertEqual(response.status_code, 200)

# AboutBookView test
class AboutBookViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_author = Author.objects.create(author_first_name='testname', author_last_name='testlastname')
        self.test_category = Category.objects.create(category_name='testcat', subcategory_name='testsubcat')
        self.test_book = Book.objects.create(
                                        isbn='789',
                                        title='test_book_title',
                                        category=self.test_category,
                                        author=self.test_author,
                                        description='This is test',
                                        date_published='2019-01-01',
                                        page_number=160,
                                        available=True
                                        )

    def test_details(self):
        request = self.factory.get('/books/about-book/')
        request.test_book = self.test_book
        response = AboutBookView.as_view()(request, pk=self.test_book.isbn)
        self.assertEqual(response.status_code, 200)