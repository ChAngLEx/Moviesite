from django.urls import path
from movie.views import ListView 


urlpatterns = [
    path('list/', ListView.as_view(), name='list'),
    ]