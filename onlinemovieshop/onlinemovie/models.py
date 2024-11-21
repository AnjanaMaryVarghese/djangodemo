from django.db import models

class Movie(models.Model):  #Database model definition
    title = models.CharField(max_length=20)
    description = models.TextField()
    language = models.CharField(max_length=20)
    year = models.DateField()
    image = models.ImageField(upload_to="images")
