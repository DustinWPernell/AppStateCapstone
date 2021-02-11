from django.db import models


# Create your models here.
class News(models.Model):
    headline = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)
