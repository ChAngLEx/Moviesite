import sys
sys.path.append(r"C:\Users\lylal\OneDrive\Desktop\my_project\FianlPro")
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from django.core.cache import cache
from user.models import User
from .models import Group, UserGroup, Event, Vote, VoteRecord, MovieList
from movie.models import Movie
from django.db.models import Q
import collections

class IndexView(View):
    def get(self, request):
        '''显示首页'''
        user = request.user.id
        groups = Group.objects.filter(group_user_id=user)

        context = {'groups': groups}

        return render(request, 'index.html', context)

class GroupCreateView(View):
    def get(self, request):

        return render(request, 'create_group.html')

    def post(self, request):

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
        group = Group.objects.create(group_user_id=group_user_id, group_name=group_name)
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

        user = request.user.id
        group = request.POST.get('group_name')

        #try:
            #group = Group.objects.get(group_name=group_name)
        
        #except Group.DoesNotExist:
            # group name不存在
            #return JsonResponse({'res':1, 'errmsg': 'group does not exist'})

        #if username in group:
            # 用户名已存在
            #return JsonResponse({'res':2, 'errmsg':'user already joined in'})

        group_id = Group.objects.get(group_name=group).id

        #user_group_id ='%d'%user1.id
        a = UserGroup.objects.create(group_id=group_id, user_id=user)
        a.save()
        #Group.objects.filter(group_name=group).update(group_user=user)

        return redirect(reverse('group:index'))


class GroupUnsubscribeView(View):
    def get(self, request):
        return render(request, 'unsubscribe.html')

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'create_group.html', {'errmsg': 'Required sign in'})

        # receive info
        #user = request.POST.get('username')
        user = request.user.id
        group = request.POST.get('group_name')

        # try:
        # group = Group.objects.get(group_name=group_name)

        # except Group.DoesNotExist:
        # group name不存在
        # return JsonResponse({'res':1, 'errmsg': 'group does not exist'})

        # if username in group:
        # 用户名已存在
        # return JsonResponse({'res':2, 'errmsg':'user already joined in'})
        #group_user_id = Group.objects.filter(group_name=group).get(group)
        #user_id = User.objects.get(username=user).id
        group_id = Group.objects.get(group_name=group).id

        UserGroup.objects.filter(Q(group_id=group_id) & Q(user_id=user)).delete()
        return redirect(reverse('group:index'))



class EventCreateview(View):

    def get(self, request):

        return render(request, 'create_event.html')

    def post(self, request):
        event_name = request.POST.get('event_name')
        event_movie = request.POST.get('event_movie')
        event_group = request.POST.get('event_group')

        #movie = request.movie
        #group = request.group
        #print("*********************************************************************************************")

        #if not all([event_name, event_movie, event_group]):
            # lack data
            #return render(request, 'create_group.html', {'errmsg': 'Requiring more information'})

        # if user.user_type == 0:
        # return render(request, 'create_group.html', {'errmsg': 'illegal user'})
        #print("_" * 122)
        #print(event_movie)
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
        event_movie_id = MovieList.objects.get(movie_name=event_movie).id
        event_group_id = Group.objects.get(group_name=event_group).id
        #print(event_movie_id, event_group_id)
        #group_user_id = '%d'%user.id
        event = Event.objects.create(event_name=event_name, event_movie_id=event_movie_id, event_group_id=event_group_id)
        event.save()

        return redirect(reverse('group:event'))

class EventView(View):
    def get(self, request):
        '''显示首页'''
        #user_id = request.user.id
        #group_id = UserGroup.objects.all()

        #events = Event.objects.filter(event_group_id=group_id)

        events = Event.objects.all()
        context = {'events': events}

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
        vote_movie = MovieList.objects.get(movie_name=vote_movie)
        vote_event = Event.objects.get(event_name=vote_event)
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

        #user_id = request.user.id
        #group_id = Group.objects.get(group_user_id=user_id).id
        #event_id = Event.objects.get(event_group_id=group_id).id
        #vote_id = Vote.objects.get(vote_event_id=event_id)
        vote_name = request.POST.get('vote_name')
        vote_id = Vote.objects.get(vote_name=vote_name).id
        vote_record = request.POST.get('vote_record')


        #if not all([vote_name, vote_record]):
            # lack data
            #return render(request, 'vote_detail.html', {'errmsg': 'Requiring more information'})

        # if user.user_type == 0:
        # return render(request, 'create_group.html', {'errmsg': 'illegal user'})

        #vote_record = VoteRecord()
        #vote_record.vote = vote_name
        #vote_record.vote_record = vote_record
        #vote_id = 1
        #vote_record = 1
        if vote_record == 1:
            vote_result = 1
        else:
            vote_result = 0
        vote_record = VoteRecord.objects.create(vote_record=vote_result, vote_id=vote_id)
        vote_record.save()

        return redirect(reverse('group:vote_record'))



class VoteRecordView(View):
    def get(self, request):


        records = VoteRecord.objects.all()

        context = {"Yes": 0, "No": 0}
        for record in records:
            if record.vote_record:
                context["Yes"] += 1
            else:
                context["No"] += 1

        return render(request, 'vote_record.html', context)   



