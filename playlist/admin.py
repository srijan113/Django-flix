from django.contrib import admin
from .models import (Playlist, PlaylistItem, 
                        TVShowProxy, TVShowSeasonProxy, 
                        MovieProxy,PlaylistRelated)

from tags.admin import TaggedItemInlineAdmin

class MovieProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInlineAdmin]
    fields = ['title', 'description', 'video', 'slug', 'status', 'category']
    list_display = ['title']
    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()


admin.site.register(MovieProxy, MovieProxyAdmin)

class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInlineAdmin,SeasonEpisodeInline]
    list_display = ['title', 'parent', 'status', 'category']

    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()

admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)


class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'status', 'category']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInlineAdmin,TVShowSeasonProxyInline]
    fields = ['title', 'description', 'video', 'slug', 'status', 'category']
    list_display = ['title']
    class Meta:
        model = TVShowProxy

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.SHOW)
admin.site.register(TVShowProxy, TVShowProxyAdmin)



class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    fk_name = 'playlist'
    extra = 0


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']
    inlines = [PlaylistRelatedInline, PlaylistItemInline, TaggedItemInlineAdmin]
    fields = ['title', 'description','slug', 'status']

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(Playlist, PlaylistAdmin)