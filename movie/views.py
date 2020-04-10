from django.shortcuts import render
from django.views.generic import View
from .models import Movie
from group.models import Group

class ListView(View):
    '''列表页'''
    def get(self, request):
        '''显示列表页'''

        # 获取商品的分类信息
        movies = Movie.objects.all()
        groups = Group.objects.all()

        # 组织模板上下文
        context = {'movies':movies,
                   'groups':groups,
                   }

        # 使用模板
        return render(request, 'list.html', context)

