from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from tags.models import TaggedItem


class Category(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem, related_query_name='category')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


    def get_absolute_url(self):
        return f"/category/{self.slug}/"

    def __str__(self):
        return self.title