from django.urls import path
from group.views import IndexView, VoteRecordView, EventView, VoteListView, VoteDetailView, GroupCreateView, \
    GroupJoinView, GroupUnsubscribeView, EventCreateview, VoteCreateview


urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('vote_record/', VoteRecordView.as_view(), name='vote_record'),
    path('event/', EventView.as_view(), name='event'),
    path('vote/', VoteListView.as_view(), name='vote'),
    path('vote_detail/', VoteDetailView.as_view(), name='vote_detail'),
    path('create_group/', GroupCreateView.as_view(), name='create_group'),
    path('join_group/', GroupJoinView.as_view(), name='join_group'),
    path('unsubscribe/', GroupUnsubscribeView.as_view(), name='unsubscribe'),
    path('create_event/', EventCreateview.as_view(), name='create_event'),
    path('create_vote/', VoteCreateview.as_view(), name='create_vote'),

    ]