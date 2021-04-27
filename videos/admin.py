from django.contrib import admin
from .models import Video, AllVideoProxy, PublishedVideoProxy, LiveVideoProxy


class AllVideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'live', 'status']
    list_filter = ['status']
    search_fields = ['video_id']
    readonly_fields = ['id', 'publish_timestamp']

    class Meta:
        model = AllVideoProxy

admin.site.register(AllVideoProxy, AllVideoProxyAdmin)


class PublishedVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'live', 'status']
    list_filter = ['status']
    search_fields = ['video_id']
    readonly_fields = ['id', 'publish_timestamp']

    class Meta:
        model = PublishedVideoProxy

    def get_queryset(self, request):
        return PublishedVideoProxy.objects.filter(status=Video.VideoStatus.PUBLISH)


admin.site.register(PublishedVideoProxy, PublishedVideoAdmin)



class LiveVideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'live', 'status']
    list_filter = ['status']
    search_fields = ['video_id']
    readonly_fields = ['id', 'publish_timestamp']

    class Meta:
        model = LiveVideoProxy

    def get_queryset(self, request):
        return PublishedVideoProxy.objects.filter(live=True)


admin.site.register(LiveVideoProxy, LiveVideoProxyAdmin)