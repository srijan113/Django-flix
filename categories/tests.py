from django.test import TestCase
from .models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        self.obj = Category.objects.create(title = "Horror")
        self.a = Category.objects.create(title = "Horror")
        self.b = Category.objects.create(title = "Horror", active=False)

    def test_category_number(self):
        a = Category.objects.all().count()
        self.assertEqual(a, 3)

    def test_active_true(self):
        self.assertTrue(self.a.active)

    def test_active_false(self):
        self.assertFalse(self.b.active)