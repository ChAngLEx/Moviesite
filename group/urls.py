from django.urls import path
from group.views import IndexView, VoteRecordView, EventView, VoteView


urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('event/vote/vote_record/', VoteRecordView.as_view(), name='vote_record'),
    path('event/', EventView.as_view(), name='event'),
    path('event/vote/', VoteView.as_view(), name='vote'),
    ]