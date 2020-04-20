from django.db import models

class Movie(models.Model):
    class Meta:
        db_table = 'df_movie'
        verbose_name = 'Movie'
        verbose_name_plural = verbose_name

    movie_name = models.CharField(max_length=50)
    movie_link = models.URLField(max_length=200, verbose_name='urls')
    movie_image = models.ImageField(upload_to='movies', verbose_name='movie images')

class Image(models.Model):
    class Meta:
        db_table = 'df_image'
        verbose_name = 'Image'
        verbose_name_plural = verbose_name

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name='movie')
    image = models.ImageField(upload_to='movies', verbose_name='images path')
