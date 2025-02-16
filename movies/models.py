from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    review = models.TextField()
    poster = models.ImageField(upload_to="movie_posters/")

    def __str__(self):
        return self.title
