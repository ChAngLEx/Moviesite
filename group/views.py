from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection
from django.core.cache import cache
from utils.mixin import LoginRequiredMixin
from user.models import User
from .models import Group, UserGroup, Event, Vote, VoteRecord
from movie.models import Movie

class IndexView(View):
    def get(self, request):
        '''显示首页'''
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')
        
        if context is None:
            print('设置缓存')
            # 缓存中没有数据
            # 获取商品的种类信息
            movies = Movie.objects.all()
            groups = Group.objects.all()

            context = {'movies': movies,
                       'groups': groups,
                       }
            # 设置缓存
            # key  value timeout
            cache.set('index_page_data', context, 3600)
    

        return render(request, 'index.html', context)

class GroupCreateView(View):

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'res':0, 'errmsg':'Required sign in'})

        if user.user_type == 0:
            return JsonResponse({'res':1, 'errmsg': 'illegal user'})
        
        group_name = request.POST.get('group_name')

        try:
            group = Group.objects.get(group_name=group_name)
        
        except Group.DoesNotExist:
            # group name不存在
            group = None

        if group:
            # 用户名已存在
            return JsonResponse({'res':2, 'errmsg':'group name illegal'})
        
       
        group = Group.objects.create_group(group_name, group_moderator, group_user)
        group.save()

        return JsonResponse({'res':3, 'message':'Created'})

class GorupJoinView(View):

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0, 'errmsg':'Required sign in'})

        #receive info
        username = request.POST.get('username')
        group_name = request.POST.get('group_name')

        try:
            group = Group.objects.get(group_name=group_name)
        
        except Group.DoesNotExist:
            # group name不存在
            return JsonResponse({'res':1, 'errmsg': 'group does not exist'})

        if username in group:
            # 用户名已存在
            return JsonResponse({'res':2, 'errmsg':'user already joined in'})
        
        conn = get_redis_connection('default')
        group_key = 'group_%d'%user.id

        conn.hset(group_key, group_name, username)

        return JsonResponse({'res':3, 'message':'Joined in'})

class GroupUnsubscribeView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:

            return JsonResponse({'res':0, 'errmsg':'Not Signed in'})

        username = request.POST.get('username')
        group_name = request.POST.get('group_name')

        if not username:
            
            return JsonResponse({'res':1, 'errmsg':'illegal username'})

        try:
            username = User.objects.get(username=username)

        except User.DoesNotExist:
            
            return JsonResponse({'res':2, 'errmsg': 'User does not exist'})
        
        try:
            group_name = Group.objects.get(group_name=group_name)

        except Group.DoesNotExist:
            
            return JsonResponse({'res':3, 'errmsg': 'Group does not exist'})

        conn = get_redis_connection('default')
        group_key = 'group_%d'%user.id

        conn.hdel(group_key, username)    

        return JsonResponse({'res':4, 'message': 'Unsubscribe!'})


class EventCreateview(View):

    def post(self, request):
        user = request.user
        group = request.group

        if not user.is_authenticated:
            return JsonResponse({'res':0, 'errmsg':'Required sign in'})


        event_name = request.POST.get('event_name')
        event_group = request.POST.get('event_group')
        event_movie = request.POST.get('event_movie')

        try:
            group = Group.objects.get(group_name=group_name)
        
        except Group.DoesNotExist:
            # group name不存在
            return JsonResponse({'res':0, 'errmsg': 'Group does not exist' })

        try:
            movie = Movie.objects.get(movie_name=movie_name)

        except Movie.DoesNotExist:

            return JsonResponse({'res':1, 'errmsg': 'Movie does not exist'})
     
        try:
            event = Event.objects.get(event_name=event_name)
        
        except Event.DoesNotExist:
            # group name不存在
            event = None
        
        if event:
            # 名已存在
            return JsonResponse({'res':2, 'errmsg':'event name illegal'})

        conn = get_redis_connection('default')
        event_key = 'event_%'%group_id

        conn.hset(event_key, event_name, event_movie)

        return JsonResponse({'res':3, 'message':'Event created'})

class EventView(View):
    def get(self, request):
        '''显示首页'''
        # 尝试从缓存中获取数据
        context = cache.get('event_page_data')
        
        if context is None:
            print('设置缓存')
            # 缓存中没有数据

            events = Event.objects.all()
            groups = Group.objects.all()

            context = {'events': events,
                       'groups': groups,
                       }
            # 设置缓存
            # key  value timeout
            cache.set('index_page_data', context, 3600)
    

        return render(request, 'event.html', context)

class VoteCreateview(View):
    def post(self, request):
        user = request.user
        event = request.event
        if not user.is_authenticated:
            return JsonResponse({'res':0, 'errmsg':'Required sign in'})


        vote_event = request.POST.get('vote_event')
        close_time = request.POST.get('close_time')
        open_time = request.POST.get('open_time')
        vote_movie = request.POST.get('vote_movie')

        try:
            event = Event.objects.get(event_name=event_name)
        
        except Event.DoesNotExist:
            # event name不存在
            return JsonResponse({'res':0, 'errmsg': 'Event does not exist' })

        try:
            movie = Movie.objects.get(movie_name=movie_name)

        except Movie.DoesNotExist:

            return JsonResponse({'res':1, 'errmsg': 'Movie does not exist'})
     
        try:
            vote = Vote.objects.get(id=id)
        
        except Event.DoesNotExist:
            # group name不存在
            vote = None
        
        if vote:
            # id已存在
            return JsonResponse({'res':2, 'errmsg':'vote already exist'})

        conn = get_redis_connection('default')
        vote_key = 'vote_%d'%event.id

        conn.hset(vote_key, vote_event, close_time, open_time, vote_movie)

class VoteView(View):
    def get(self, request):
        '''显示首页'''
        # 尝试从缓存中获取数据
        context = cache.get('vote_page_data')
        
        if context is None:
            print('setting cache')
            # 缓存中没有数据
            
            votes = Vote.objects.all()
            events = Event.objects.all()
            

            context = {'votes': votes,
                       'events': events,
                       }
            # 设置缓存
            # key  value timeout
            cache.set('vote.html', context, 3600)
    

        return render(request, 'event.html', context)

class VoteRecordView(View):
    def vote_record(self, request):
        group_list = VoteRecord.objects.all()
        context = get_vote_record_common_data(request,vote_record)

        return render(request, 'vote_record.html', context)   






# Create your views here.

