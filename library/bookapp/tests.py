from django.test import TestCase
from .models import Book


class ProjectTestCase(TestCase):

    def create_project(self, title="myproject3", description="my_test", time_spent="2:30"):
        return Book.objects.create(title="myproject3", description="my_test", time_spent="2:30")

    def test_project_title(self):
        project = self.create_project()

        self.assertEqual(project.title, "myproject2")