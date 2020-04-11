import sys
sys.path.append(r"C:\Users\lylal\OneDrive\Desktop\my_project\FianlPro")
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from django.core.cache import cache
from user.models import User
from .models import Group, UserGroup, Event, Vote, VoteRecord
from movie.models import Movie

class IndexView(View):
    def get(self, request):
        '''显示首页'''
        groups = Group.objects.all()

        context = {'groups': groups}

        return render(request, 'index.html', context)

class GroupCreateView(View):
    def get(self, request):

        return render(request, 'create_group.html')

    def post(self, request):
        group_user = request.POST.get('user_name')
        group_name = request.POST.get('group_name')
        user = request.user


        if not user.is_authenticated:
            return render(request, 'create_group.html', {'errmsg': 'Required sign in'})

        #if not all([group_user, group_name]):
            # lack data
            #return render(request, 'create_group.html', {'errmsg': 'Requiring more information'})
        
        #if user.user_type == 0:
            #return render(request, 'create_group.html', {'errmsg': 'illegal user'})

        try:
            group = Group.objects.get(group_name=group_name)

        except Group.DoesNotExist:
            # group name不存在
            group = None

        if group:
            # 用户名已存在
            return render(request, 'create_group.html', {'errmsg': 'group name illegal'})


        group_user_id = '%d'%user.id
        group = Group.objects.create(group_user_id=group_user_id, group_name=group_name, group_user=group_user)
        group.save()

        return redirect(reverse('group:index'))

class GroupJoinView(View):
    def get(self, request):

        return render(request, 'join_group.html')

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'create_group.html', {'errmsg': 'Required sign in'})

        #receive info
        user = request.POST.get('username')
        group = request.POST.get('group_name')

        #try:
            #group = Group.objects.get(group_name=group_name)
        
        #except Group.DoesNotExist:
            # group name不存在
            #return JsonResponse({'res':1, 'errmsg': 'group does not exist'})

        #if username in group:
            # 用户名已存在
            #return JsonResponse({'res':2, 'errmsg':'user already joined in'})

        Group.objects.filter(group_name=group).update(group_user=user)

        return redirect(reverse('group:index'))


class GroupUnsubscribeView(View):
    def get(self, request):
        return render(request, 'unsubscribe.html')

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'create_group.html', {'errmsg': 'Required sign in'})

        # receive info
        user = request.POST.get('username')
        group = request.POST.get('group_name')

        # try:
        # group = Group.objects.get(group_name=group_name)

        # except Group.DoesNotExist:
        # group name不存在
        # return JsonResponse({'res':1, 'errmsg': 'group does not exist'})

        # if username in group:
        # 用户名已存在
        # return JsonResponse({'res':2, 'errmsg':'user already joined in'})

        Group.objects.filter(group_name=group).update(group_user=None)
        return redirect(reverse('group:index'))

class EventCreateview(View):

    def get(self, request):

        return render(request, 'create_event.html')

    def post(self, request):
        event_name = request.POST.get('event_name')
        event_movie = request.POST.get('movie_name')
        event_group = request.POST.get('group_name')

        #movie = request.movie
        #group = request.group


        if not all([event_name, event_movie, event_group]):
            # lack data
            return render(request, 'create_group.html', {'errmsg': 'Requiring more information'})

        # if user.user_type == 0:
        # return render(request, 'create_group.html', {'errmsg': 'illegal user'})

        try:
            event = Event.objects.get(event_name=event_name)

        except Event.DoesNotExist:
            # group name不存在
            event = None

        if event:
            # 用户名已存在
            return render(request, 'create_group.html', {'errmsg': 'group name illegal'})

        #event = Event()
        #event.event_name = event_name
        #event.event_movie = event_movie
        #event.event_group = event_group

        #group_user_id = '%d'%user.id
        event = Event.objects.create(event_name=event_name, event_movie=event_movie, event_group=event_group)
        event.save()

        return redirect(reverse('group:event'))

class EventView(View):
    def get(self, request):
        '''显示首页'''
        # 尝试从缓存中获取数据
        context = cache.get('event_page_data')
        
        if context is None:
            print('Setting Cache')
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

    def get(self, request):

        return render(request, 'create_vote.html')

    def post(self, request):
        vote_movie = request.POST.get('vote_movie')
        vote_name = request.POST.get('vote_name')
        open_time = request.POST.get('open_time')
        close_time = request.POST.get('close_time')
        vote_event = request.POST.get('vote_event')

        #vote = request.vote

        if not all([vote_movie,vote_name, open_time,close_time, vote_event,]):
            # lack data
            return render(request, 'create_vote.html', {'errmsg': 'Requiring more information'})

        # if user.user_type == 0:
        # return render(request, 'create_group.html', {'errmsg': 'illegal user'})

        #try:
            #vote = Vote.objects.get(vote_name=vote_name)

        #except Vote.DoesNotExist:
            # group name不存在
            #Vote = None

        #if vote:
            # 用户名已存在
            #return render(request, 'create_vote.html', {'errmsg': 'vote name illegal'})

        #vote = Vote()
        #vote.vote_movie = vote_movie
        #vote.open_time = open_time
        #vote.close_time = close_time
        #vote.vote_event = vote_event
        vote = Vote.objects.create(vote_name=vote_name, vote_movie=vote_movie, close_time=close_time, vote_event=vote_event)
        vote.save()

        return redirect(reverse('group:vote'))

class VoteListView(View):
    def get(self, request):
        '''显示列表页'''

        votes = Vote.objects.all()

        context = {'votes': votes}

        return render(request, 'vote.html', context)

class VoteDetailView(View):
    def get(self, request):

        return render(request, 'vote_detail.html')

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': 'User is not signed in!'})

        vote_name = request.POST.get('vote_name')
        vote_record = request.POST.get('vote_record')


        if not all([vote_name, vote_record]):
            # lack data
            return render(request, 'vote_detail.html', {'errmsg': 'Requiring more information'})

        # if user.user_type == 0:
        # return render(request, 'create_group.html', {'errmsg': 'illegal user'})

        vote_record = VoteRecord()
        vote_record.vote = vote_name
        vote_record.vote_record = vote_record

        return redirect(reverse('group:vote_detail'))


class VoteRecordView(View):
    def get(self, request):


        records = VoteRecord.objects.all()

        context = {'records': records}

        return render(request, 'vote_record.html', context)   






# Create your views here.

