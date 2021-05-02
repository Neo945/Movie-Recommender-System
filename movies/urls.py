from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    add_data,
    all_movies,
    director_list,
    genre_list,
    movie_details,
    genre_movie,
    movie_search,
    create_movie,
    recommend,
    get_popular,
    get_genre_popular
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
    path('api/recommend',recommend),
    path('api/popular',get_popular),
    path('api/popular/genre/movie',get_genre_popular),
    path('add/',add_data)
]
