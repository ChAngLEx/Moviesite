from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from user.models import User
from group.models import Group, Event, Vote
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
import re
import time

class RegisterView(View):
    '''Functions: register'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # lack data
            return render(request, 'register.html', {'errmsg': 'Requiring more information'})

        # check email format 
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            
            return render(request, 'register.html', {'errmsg': 'Email Format is not correct'})
        
        
        if allow != 'on':
            
            return render(request, 'register.html', {'errmsg': 'Please consent user agreement'})

        # check the user name is or is not correct
        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': 'User name has been registered'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()

        return redirect(reverse('user:login'))


# /user/login
class LoginView(View):
    '''Fuctions: Login'''
    def get(self, request):
        '''显示登录页面'''
        
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'Requiring more infomation'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                # 跳转到next_url
                next_url = request.GET.get('next', reverse('movie:list'))
                
                response = redirect(next_url) # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # remenber user name
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # return response
                return response
            
        else:
            # User name or password is not correct
            return render(request, 'login.html', {'errmsg':'User name or password is not correct'})

# /user/logout
class LogoutView(View):
    '''退出登录'''
    
    def get(self, request):
        '''Fuction:Logout'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('user:login'))

# /user
class UserInfoView(LoginRequiredMixin, View):
    '''User Center: info page'''
    
    def get(self, request):
        '''显示'''
        # Django会给request对象添加一个属性request.user
        # 如果用户未登录->user是AnonymousUser类的一个实例对象
        # 如果用户登录->user是User类的一个实例对象
        # request.user.is_authenticated()

        # 获取用户的个人信息
        user = request.user
        context = {'user':user}


        return render(request, 'user_center_info.html', context)
        
class UserGroupView(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user
        groups = Group.objects.all

        for group in gruops:
            group = group_name

        context = {'group':groups}

        return render(request, 'index.html', context)






