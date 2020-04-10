from django.db import models

class Movie(models.Model):
    class Meta:
        db_table = 'df_movie'
        verbose_name = 'Movie'
        verbose_name_plural = verbose_name

    movie_name = models.CharField(max_length=50)
    trailer_links = models.CharField(max_length=100) 
    review_links = models.CharField(max_length=100)

