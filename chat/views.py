from django.shortcuts import render, redirect, get_object_or_404
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
                pass
        except User.DoesNotExist:
            # todo: POSTの2重送信を回避したうえでエラーメッセージを表示させる方法を考える
            #   1. Getメソッドのクエリストリングに埋め込む
            #   2. エラーメッセージ表示用のリダイレクト先URLを作成する
            #   3. そのほか何かいい方法ないか？
            pass
        return render(request, 'chat/login.html',
                      {'error_message': 'IDが登録されていないか、パスワードが間違っています。', })
    else:  # GET
        return render(request, 'chat/login.html')


def register(request):
    # return HttpResponse('Register View')
    template_reg = 'chat/register.html'
    template_regd = 'chat/register.html'
    if request.method == 'POST':
        user_id = request.POST['id']
        user_passwd = request.POST['passwd']
        user_passwd_renter = request.POST['passwd_renter']
        # check id collision
        try:
            User.objects.get(pk=user_id)
            return render(request, template_reg,
                          {'error_message': '既に使用されているか、無効な文字列のため使用できないIDです。'})
        except User.DoesNotExist:
            pass
        # check passwd
        if user_passwd == '':
            return render(request, template_reg,
                          {'error_message': 'パスワードが入力されていません。'})
        # check renter passwd
        if user_passwd != user_passwd_renter:
            return render(request, template_reg,
                          {'error_message': '確認用パスワードが一致しません。'})
        # make new user
        u = User(user_id=user_id, user_passwd=user_passwd)
        u.save()
        return redirect('chat:registered')
    else:  # GET
        return render(request, 'chat/register.html')


def registered(request):
    return render(request, 'chat/registered.html')


def mypage(request):
    return HttpResponse('MyPage View')
