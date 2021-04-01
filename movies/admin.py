from movies.models import Director, Genre, Movie, MovieLikes, movie_genre
from django.contrib import admin

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(MovieLikes)
admin.site.register(movie_genre)
