from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username

class History(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    movies = models.ForeignKey('movies.Movie',on_delete=models.CASCADE)
    user_rating = models.IntegerField(null=False,validators=[MaxValueValidator(10),MinValueValidator(1)])
    comments = models.TextField(max_length=255,blank=True,null=True)
    def __str__(self) -> str:
        return self.user.user.username + ': ' + self.movies.name + ' ' + f'{self.user_rating}'