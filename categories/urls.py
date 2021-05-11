from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryList.as_view(), name="category_list"),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),


]