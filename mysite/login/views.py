from django.shortcuts import render,redirect
from login import models
from login import forms

# Create your views here.
def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
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
                    if user.password == password:
                        return redirect('/index/')
                    else:
                        mess = '密码错误，请重新输入'
                except:
                    mess = '账号不存在'
            return render(request, 'login/login.html',locals())
    return render(request, 'login/login.html')

def register(request):
    pass
    return render(request,'login/register.html')

def logout(request):
    pass
    return redirect('/index/')

