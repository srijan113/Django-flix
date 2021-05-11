from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.query_utils import select_related_descend


class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list('slug', flat=True))
        return sorted(list(tags_set))



class TaggedItem(models.Model):
    slug = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = TaggedItemManager()


    def save(self, *args, **kwargs):
        new_slug = self.slug
        self.slug = new_slug.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.slug