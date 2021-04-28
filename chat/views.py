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
            # todo: POSTの2重送信を回避したうえでエラーメッセージを表示させる方法を考える
            #   1. Getメソッドのクエリストリングに埋め込む
            #   2. エラーメッセージ表示用のリダイレクト先URLを作成する
            #   3. そのほか何かいい方法ないか？
            return render(request, 'chat/login.html',
                          {'error_message': 'IDが登録されていないか、パスワードが間違っています。', })
    else:
        return render(request, 'chat/login.html')


def mypage(request):
    return HttpResponse('MyPage View')


def register(request):
    return HttpResponse('Register View')
