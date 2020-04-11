import sys
sys.path.append(r"C:\Users\lylal\OneDrive\Desktop\my_project\FianlPro")
from django.shortcuts import render
from django.views.generic import View
from movie.models import Movie

class ListView(View):
    '''列表页'''
    def get(self, request):
        '''显示列表页'''

        movies = Movie.objects.all()

        context = {'movies':movies}

        return render(request, 'list.html', context)

