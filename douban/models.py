from django.db import models

# Create your models here.

class Movie(models.Model):
    top = models.CharField(max_length=4)
    name = models.CharField(max_length=128)
    director = models.CharField(max_length=256)
    time = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    style = models.CharField(max_length=128)
    mark = models.CharField(max_length=10)

class Dj(models.Model):
    title = models.CharField(max_length=128)
    price = models.FloatField()
    imgurl = models.CharField(max_length=128)
    url=models.CharField(max_length=128)
    info = models.CharField(max_length=8192)