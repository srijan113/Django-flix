from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.MovieProxyViewList.as_view(), name = "movie_list"),
    path('movies/<slug:slug>/', views.MovieProxyViewDetail.as_view(), name = "movie_detail"),
    path('show/', views.TVShowProxyViewList.as_view(), name = "tv_show"),
    path('show/<slug:slug>/', views.TVShowProxyViewDetail.as_view(), name = "tv_show_detail"),
    path('show/<slug:slug>/season/', views.TVShowProxyViewDetail.as_view(), name = "tv_show_season_list"),
    path('show/<slug:showSlug>/season/<slug:seasonSlug>/', views.TVShowSeasonProxyViewDetail.as_view(), name = "tv_show_season_detail"),
    path('', views.FeturedPlaylistViewList.as_view(), name = 'playlist_list'),
    path('media/<int:pk>/', views.FeturedPlaylistViewDetail.as_view(), name = 'playlist_detail'),



]
