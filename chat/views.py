from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User


def login(request):
    # return HttpResponse('Login View')
    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            user_passwd = request.POST['passwd']
            u = User.objects.get(pk=user_id)
            if user_passwd == u.user_passwd:
                return redirect('chat:mypage')
            else:
                return redirect('chat:login')
        except User.DoesNotExist:
            return redirect('chat:login')
    else:
        return render(request, 'chat/login.html')


def mypage(request):
    return HttpResponse('MyPage View')


def register(request):
    return HttpResponse('Register View')
