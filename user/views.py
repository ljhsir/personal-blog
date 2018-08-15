import random
import string
import time
from django.contrib import auth
from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse   # 反向
from .forms import LoginForm, RegForm, ChangeNickNameForm, BindEmailForm, ChangePasswordForm, ForgetPasswordForm
from .models import Profile
from django.http import JsonResponse

def login(request):
    if request.method == "POST":     #判断是否为POST请求
        login_form = LoginForm(request.POST)  # 表单实例化，并带有数据
        if login_form.is_valid():   # 验证表单数据是否合法
            user = login_form.cleaned_data['user']
            auth.login(request, user)
             # 用户登录，返回前一页 
            return redirect(request.GET.get('from', reverse('home')))
        else:  # 携带错误信息返回登陆页面
            context = {}
            context['login_form'] = login_form
            return render(request, 'user/login.html', context)
    else:
        login_form = LoginForm()  # 不是POST请求则空表单返回  

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home'))) 

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():   # 验证表单数据是否合法
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:  # 携带错误信息返回登陆页面
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == "POST":     #判断是否为POST请求
        reg_form = RegForm(request.POST)  # 表单实例化，并带有数据
        if reg_form.is_valid():   # 验证表单数据是否验证通过
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))  # 用户登录，返回主页 
    else:
        reg_form = RegForm()  # 不是POST请求则空表单返回 是加载页面 
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def get_user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method =='POST':
        form = ChangeNickNameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user = request.user)
            profile.nickname=nickname_new
            profile.save()
            return redirect(return_to)
    else:   
        form = ChangeNickNameForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '确认修改'
    context['return_back_url'] = return_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method =='POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            #绑定邮箱
            request.user.save()
            #清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email !='':
         # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            
            # 发送邮件
            send_mail(
                'Myblog绑定邮箱',
                '验证码：%s' % code,
                '1401818504@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method =='POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(

                password)
            user.save()
            auth.logout(request)
            return redirect(return_to)
    else:   
        form = ChangePasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '确认修改'
    context['return_back_url'] = return_to
    return render(request, 'form.html', context)

def forget_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forget_password.html', context)

