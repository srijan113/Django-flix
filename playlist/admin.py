from django.contrib import admin
from .models import Playlist, PlaylistItem



class PlaylistItemAdmin(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']
    inlines = [PlaylistItemAdmin]

    class Meta:
        model = Playlist

admin.site.register(Playlist, PlaylistAdmin)