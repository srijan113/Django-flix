from django.db import reset_queries
from django.db.models import query
from django.db.models.query_utils import Q, select_related_descend
from django.shortcuts import render
from django.http import Http404, request
from django.views import View
from django.views import generic
from .models import MovieProxy, TVShowProxy, Playlist, TVShowSeasonProxy
from django.utils import timezone
from videos.models import VideoStatus
from .mixins import PlaylistMixin




class MovieProxyViewList(PlaylistMixin, generic.ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

class MovieProxyViewDetail(PlaylistMixin, generic.DetailView):
    template_name = 'playlist/movie_detail.html'
    queryset = MovieProxy.objects.all()


class TVShowProxyViewList(PlaylistMixin, generic.ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV Show"

class TVShowProxyViewDetail(PlaylistMixin, generic.DetailView):
    template_name = 'playlist/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()

class TVShowSeasonProxyViewDetail(PlaylistMixin, generic.DetailView):
    template_name = 'playlist/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(status= VideoStatus.PUBLISH, timestamp__lte=now, parent__slug__iexact=show_slug, slug__iexact=season_slug)
        # qs = self.get_queryset().filter(parent__slug__iexact=show_slug, slug__iexact = season_slug)
        # if not qs.count() == 1:
        #     raise Http404
        # return qs.first()
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(parent__slug__iexact=show_slug, slug__iexact=season_slug).published()
            obj = qs.first()
        except:
            obj = None
            raise Http404
        return obj



class FeturedPlaylistViewList(PlaylistMixin, generic.ListView):
    template_name = 'playlist/fetured_list.html'
    queryset = Playlist.objects.featured_playlist()
    title = "Fetured Playlist"


class FeturedPlaylistViewDetail(PlaylistMixin, generic.DetailView):
    template_name = 'playlist/playlist_detail.html'
    queryset = Playlist.objects.all()


class SearchViewList(PlaylistMixin, generic.ListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        if query is not None:
            context['title'] = f"Search for {query}"
        else:
            context['title'] = "Perform a search"
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Playlist.objects.all().movie_or_show().search(query = query)