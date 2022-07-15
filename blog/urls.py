from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('followers_count/', views.followers_count, name='followers_count'),
    path('index/', views.index, name='index'),
]