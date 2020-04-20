import sys
sys.path.append(r"C:\Users\lylal\OneDrive\Desktop\my_project\FianlPro")
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from movie.models import Movie
from django.conf import settings
import os

class ListView(View):
    '''列表页'''
    def get(self, request):
        '''显示列表页'''

        movies = Movie.objects.all()
        img_list = []
        for static_path in settings.STATICFILES_DIRS:
            img_list.extend(os.listdir(os.path.join(static_path, 'images/movies')))

        context = {'movies': movies,
                   'img_list': img_list}

        return render(request, 'list.html', context)

#class PullMovieView(View):
    #def get(self, request):

        #return render(request, 'pull_movie.html')

    #def post(self, request):

        #movie_name = request.POST.get('movie_name')
        #links = request.POST.get('links')
        #review_links = request.POST.get('review_links')

        #movie = Movie.objects.create(movie_name=movie_name, trailer_links=trailer_links, review_links=review_links)
        #movie.save()

        #return redirect(reverse('movie:list'))