from django.urls import path
from .views import (
    all_movies
)
app_name = 'movies'

urlpatterns = [
    path('api/movie',all_movies),
]
