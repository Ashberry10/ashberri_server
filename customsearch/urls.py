from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.search_users, name='search_users'),
    path('posts/', views.search_posts, name='search_posts'),
]
