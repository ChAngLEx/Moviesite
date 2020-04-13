import sys
sys.path.append(r"C:\Users\lylal\OneDrive\Desktop\my_project\FianlPro")
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from movie.models import Movie

class ListView(View):
    '''列表页'''
    def get(self, request):
        '''显示列表页'''

        movies = Movie.objects.all()

        context = {'movies': movies}

        return render(request, 'list.html', context)

class PullMovieView(View):
    def get(self, request):

        return render(request, 'pull_movie.html')

    def post(self, request):

        movie_name = request.POST.get('movie_name')
        trailer_links = request.POST.get('trailer_links')
        review_links = request.POST.get('review_links')

        movie = Movie.objects.create(movie_name=movie_name, trailer_links=trailer_links, review_links=review_links)
        movie.save()

        return redirect(reverse('movie:list'))