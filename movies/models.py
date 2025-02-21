from uuid import uuid4
from django.db import models


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    
    title = models.CharField(max_length=255, unique=True)
    director = models.CharField(max_length=255)
    genre = models.CharField(max_length=16)
    year = models.IntegerField()
    review = models.TextField()
    poster = models.URLField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"
        ordering = ["title"]

    def __str__(self):
        return f"Movie: {self.title}"
