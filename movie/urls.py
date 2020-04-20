from django.urls import path
from movie.views import ListView
from django.conf.urls import url
from django.views.static import serve
from FianlPro.settings import MEDIA_ROOT

urlpatterns = [
    # path('list/', ListView.as_view(), name='list'),
    url(r'list/', ListView.as_view(), name='list'),
    # path('pull_movie/', PullMovieView.as_view(), name='pull_movie'),
    url(r'^upload/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
