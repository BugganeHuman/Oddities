from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError

def rating_validator(value):
    if value % Decimal("0.5") != 0:
        raise ValidationError ("the rating must be a multiple of 0.5, for example 6 or 6.5")



class Title(models.Model):

    class TitleCategory(models.TextChoices):
        MOVIE = "MV", "Movie"
        SERIES = "SR", "Series"
        ANIME = "ANM", "Anime"
        CARTOON = "CRT", "Cartoon"
        LEGAL = "LG", "Legal case"
        VIDEO = "VD", "Youtube video ot other"
        READING = "READ", "Written content"

    class TitleStatus(models.TextChoices):
        DONE = "DONE", "Done"
        DROPPED = "DROP", "Dropped"
        REVISIT = "RVS", "Revisit or Finish"
        WATCHING = "WATCH", "Watching"

    name = models.CharField(max_length=300)
    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField(null=True, blank=True)
    director = models.CharField(max_length=200)
    category = models.CharField(max_length=7, choices=TitleCategory.choices,
        default=TitleCategory.SERIES)
    cover = models.URLField()
    start_watch = models.DateField()
    end_watch = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=TitleStatus.choices, default=TitleStatus.DONE)
    review = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10), rating_validator])


