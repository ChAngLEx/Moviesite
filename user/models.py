from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'df_user'
        verbose_name = 'Use'
        verbose_name_plural = verbose_name

    USER_TYPE = ((0, 'user'),
        (1, 'moderator'))
    user_type = models.SmallIntegerField(choices=USER_TYPE, default=0, verbose_name='UserType')
    

