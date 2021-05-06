from django.contrib import admin
from .models import Playlist, PlaylistItem, TVShowProxy, TVShowSeasonProxy, MovieProxy
from tags.admin import TaggedItemInlineAdmin

class MovieProxyAdmin(admin.ModelAdmin):
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
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent', 'status', 'category']

    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()

admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)


class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'states', 'category']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TVShowSeasonProxyInline]
    fields = ['title', 'description', 'video', 'slug', 'status', 'category']
    list_display = ['title']
    class Meta:
        model = TVShowProxy

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.SHOW)
admin.site.register(TVShowProxy, TVShowProxyAdmin)


class PlaylistItemAdmin(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']
    inlines = [PlaylistItemAdmin]

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(Playlist, PlaylistAdmin)