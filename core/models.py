from django.db import models

class Title(models.Model):
    name = models.CharField(max_length=300)
    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField(null=True, blank=True)
    director = models.CharField(max_length=200)
    review = models.TextField()
    cover = models.URLField()
    start_watch = models.DateField()
    end_watch = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)