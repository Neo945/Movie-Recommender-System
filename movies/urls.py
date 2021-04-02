from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    all_movies,
    director_list,
    genre_list,
    movie_details,
    genre_movie,
    movie_search,
    create_movie
)
app_name = 'movies'

urlpatterns = [
    path('api/movie',all_movies),
    path('api/movie/<int:movie_id>',movie_details),
    path('api/movie/genre/<int:genre_id>',genre_movie),
    path('api/movie/search',movie_search),
    path('api/movie/create',create_movie),
    path('api/director',director_list),
    path('api/genre',genre_list),
    path('',TemplateView.as_view(template_name='login_signup.html'))
]
