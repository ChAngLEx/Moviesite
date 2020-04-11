from django.db import models
from user.models import User

class Group(models.Model):
    class Meta:
        db_table = 'df_group'
        verbose_name = 'Group'
        verbose_name_plural = verbose_name

    group_name = models.CharField(max_length=30, verbose_name='groupname')
    group_user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)
    

class MovieList(models.Model):
    class Meta:
        db_table = 'df_movielist'
        verbose_name = 'Movielist'
        verbose_name_plural = verbose_name

    movie_name = models.CharField(max_length=50)
    movie_group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Event(models.Model):
    class Meta:
        db_table = 'df_event'
        verbose_name = 'Event'
        verbose_name_plural = verbose_name

    event_name = models.CharField(max_length=50, default=1)
    event_group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    event_movie = models.ForeignKey(MovieList, on_delete=models.CASCADE, default=1)    

class Vote(models.Model):
    class Meta:
        db_table = 'df_vote'
        verbose_name = 'Vote'
        verbose_name_plural = verbose_name

    vote_movie = models.ForeignKey(MovieList, on_delete=models.CASCADE, default=1)
    vote_name = models.CharField(max_length=30, default=1)
    open_time = models.DateTimeField(auto_now_add=True)
    close_time = models.DateTimeField(auto_now=True)
    vote_event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    

class VoteRecord(models.Model):
    class Meta:
        db_table = 'df_voterecord'
        verbose_name = 'VoteRecord'
        verbose_name_plural = verbose_name
    
    VOTE_RECORD = ((1, 'Yes'),
        (0, 'No')
        )
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, default=1)
    vote_record = models.SmallIntegerField(choices=VOTE_RECORD, default=1)
    

class UserGroup(models.Model):
    class Meta:
        db_table = 'df_usergroup'
        verbose_name = 'UserGroup'
        verbose_name_plural = verbose_name

    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)




