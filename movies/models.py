from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator,MinValueValidator

User = settings.AUTH_USER_MODEL

class MovieLikes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movies = models.ForeignKey('Movie',on_delete=models.CASCADE)


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=255,null=False)
    file = models.CharField(max_length=255,null=False)
    poster = models.CharField(max_length=255,null=False)
    rating = models.FloatField(null=False,validators=[MaxValueValidator(10),MinValueValidator(1)])
    genre = models.ManyToManyField('Genre',related_name='genres',blank=True,through='movie_genre')
    director = models.ForeignKey('Director',on_delete=models.CASCADE)
    cast = models.TextField(null=False)
    likes = models.ManyToManyField(User,related_name='user_movies',through=MovieLikes)
    # upload_by = models.ForeignKey(Profile,on_delete=models.SET('Anonymous'))

    def __str__(self) -> str:
        return self.name

class movie_genre(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre',on_delete=models.CASCADE)

class Genre(models.Model):
    genre = models.CharField(max_length=255,null=False)

class Director(models.Model):
    name = models.CharField(max_length=255,null=False)