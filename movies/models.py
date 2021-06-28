from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=150)


class Movie(models.Model):
    title = models.CharField(max_length=150)
    duration = models.CharField(max_length=150)

    genres = models.ManyToManyField(Genre, related_name='movies')

    launch = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()


class Review(models.Model):
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    review = models.TextField()
    spoiler = models.BooleanField()

    movie = models.ForeignKey(
        Movie, related_name='criticism_set', on_delete=models.CASCADE
    )
    critic = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.CharField(max_length=150)

    movie = models.ForeignKey(
        Movie, related_name='comment_set', on_delete=models.CASCADE
    )

    user = models.ForeignKey(User, related_name='comment_set', on_delete=models.CASCADE)
