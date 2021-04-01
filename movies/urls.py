from django.urls import path
from .views import (
    all_movies,
    movie_details,
    genre_movie
)
app_name = 'movies'

urlpatterns = [
    path('api/movie',all_movies),
    path('api/movie/<int:movie_id>',movie_details),
    path('api/movie/genre/<int:genre_id>',genre_movie),
]
