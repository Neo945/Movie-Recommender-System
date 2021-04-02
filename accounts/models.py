from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    movies = models.ForeignKey('movies.Movie',on_delete=models.CASCADE)