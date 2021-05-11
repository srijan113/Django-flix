from tags.models import TaggedItem
from django.shortcuts import render
from  django.views import View
from .models import TaggedItem
from playlist.mixins import PlaylistMixin
from django.views import generic
from playlist.models import Playlist


class TaggedItemList(View):
    def get(self, request):
        tag_list = TaggedItem.objects.unique_list()
        context = {
            'tag_list': tag_list,
            'title': 'Tags'
        }
        return render(request, 'tags/tags_list.html', context)



class TaggedItemDetailView(PlaylistMixin, generic.ListView):
    """
    Another list view for playlist
    """

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = f"{self.kwargs.get('slug')}".title()
        return context

    def get_queryset(self):
        tag = self.kwargs.get('slug')
        return Playlist.objects.filter(tags__slug = tag).movie_or_show()