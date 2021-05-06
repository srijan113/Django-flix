
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from .models import TaggedItem



class TaggedItemInlineAdmin(GenericTabularInline):
    model = TaggedItem
    extra = 0

class TaggedItemAdmin(admin.ModelAdmin):
    fields = ['slug', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_object']

    class Meta:
        model = TaggedItem



admin.site.register(TaggedItem, TaggedItemAdmin)