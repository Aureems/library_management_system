from django.test import TestCase
# 1 variantas
# from .models import Project

# 2 variantas
from selenium import webdriver


# 1 variantas
# # Create your tests here.
# class ProjectTestCase(TestCase):
#     def create_project(self, title="modelio kuri importuojam laukai"):
#         return Project.objects.create(title="modelio kuri importuojam laukai")
#
#     def test_project_title(self):
#         project = self.create_project()
#
#         self.assertEqual(project.title, "myproject2")

# class ProjectTestCase(TestCase):
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()