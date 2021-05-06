from django.test import TestCase
from django.db.utils import IntegrityError
from .models import TaggedItem


class TaggedItemTestCase(TestCase):

    def setUp(self):
        self.tag_a = TaggedItem.objects.create(tag = "my-new-tag")
    

    def test_content_type_not_null(self):
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag = "my-new-tag")
        # self.assertIsNotNone(self.tag_a.pk)

