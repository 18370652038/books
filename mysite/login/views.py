from django.shortcuts import render,redirect
from login import models
from login import forms
from django.views.decorators.csrf import csrf_exempt
import hashlib

# Create your views here.
def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        login_from = forms.Userfrom(request.POST)
        mess = '所有字段必须全部填写'
        if login_from.is_valid():
            username = login_from.cleaned_data['username']
            password = login_from.cleaned_data['password']
            mess = '密码必须大于4位'
            if len(password) >= 4:
                username = username.strip()
                try:
                    user = models.User.objects.get(name=username)
                    if user.password == hash_cold(password):
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        return redirect('/index/')
                    else:
                        mess = '密码错误，请重新输入'
                except:
                    mess = '账号不存在'
            return render(request, 'login/login.html',locals())
    login_from = forms.Userfrom()
    return render(request, 'login/login.html',locals())

@csrf_exempt
def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查您输入的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            password1 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password != password1 :
                message = '二次密码不一样，请重新输入'
                return render(request,'login/register.html',locals())
            else:
                try:
                    same_user_name = models.User.objects.get(name=username)
                except:
                    same_user_name = False
                if same_user_name:
                    message = '用户名已存在'
                    return render(request,'login/register.html',locals())
                try:
                    same_email_name = models.User.objects.get(email=email)
                except:
                    same_email_name = False
                if same_email_name:
                    message = '邮箱以被注册'
                    return render(request,'login/register.html',locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_cold(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def hash_cold(s,salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

