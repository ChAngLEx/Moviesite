from django.contrib import admin
from .models import Group, MovieList, Event, Vote, VoteRecord, UserGroup


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_user')

@admin.register(MovieList)
class MovieListAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'movie_group')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_group', 'event_movie')    

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote_movie', 'open_time', 'close_time', 'vote_event')

@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('vote', 'vote_record')

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'user')

