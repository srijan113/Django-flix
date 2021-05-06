from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class TaggedItem(models.Model):
    slug = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    objects_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "objects_id")


    def __str__(self):
        return self.slug