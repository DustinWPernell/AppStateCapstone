from django.db import models
from datetime import datetime


# Create your models here.
class News(models.Model):
    headline = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)
    eventDate = models.DateField(default=datetime.now)
