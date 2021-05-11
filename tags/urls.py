from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaggedItemList.as_view(), name = 'tagged_list'),
    path('<slug:slug>/', views.TaggedItemDetailView.as_view(), name = 'tagged_detail'),
]