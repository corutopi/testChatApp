from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, AppToken


def login(request):
    # return HttpResponse('Login View')
    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            user_passwd = request.POST['passwd']
            u = User.objects.get(pk=user_id)
            if user_passwd == u.user_passwd:
                at = _make_apptoken(user_id)
                hrr = redirect('chat:mypage')  # HttpResponseRedirect
                hrr.set_cookie(key='app_token', value=at.app_token,
                               expires=at.ttl)
                hrr.set_cookie(key='user_id', value=at.user_id.user_id,
                               expires=at.ttl)
                return hrr
            else:
                pass
        except User.DoesNotExist:
            # todo: POSTの2重送信を回避したうえでエラーメッセージを表示させる方法を考える
            #   1. リダイレクトURLのクエリストリングに埋め込む
            #   2. エラーメッセージ表示用のリダイレクト先URLを作成する
            #   3. そのほか何かいい方法ないか？
            #   4. POSTする前にjavascriptでチェックを行う(できんのか？)
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


def _check_logged_in(func):
    """認証デコレータ"""

    def warapper(*args, **kwargs):
        request = args[0]
        user_id = request.COOKIES.get('user_id')
        app_token = request.COOKIES.get('app_token')
        try:
            at = AppToken.objects.get(user_id=User.objects.get(user_id=user_id),
                                      app_token=app_token)
        except ObjectDoesNotExist:
            return redirect('chat:login')
        return func(*args, **kwargs)

    return warapper


@_check_logged_in
def mypage(request):
    template_mypage = 'chat/mypage.html'
    user_id = request.COOKIES.get('user_id')
    return render(request, template_mypage,
                  {'user_id': user_id})


@_check_logged_in
def logout(request):
    user_id = request.COOKIES.get('user_id')
    app_token = request.COOKIES.get('app_token')
    AppToken.objects.filter(user_id=User.objects.get(user_id=user_id),
                            app_token=app_token).delete()
    hrr = redirect('chat:loggedout')  # HttpResponseRedirect
    # expire cookie
    hrr.set_cookie(key='app_token', value='',
                   expires=datetime.now() - timedelta(days=30))
    hrr.set_cookie(key='user_id', value='',
                   expires=datetime.now() - timedelta(days=30))
    return hrr


def loggedout(request):
    return render(request, 'chat/loggedout.html')


def _make_apptoken(user_id):
    """トークンを作成する"""
    TOKEN_LENGTH = 30
    TOKEN_TTL_DATE = 0.5

    us = AppToken.objects.filter(user_id=user_id)
    token_list = [u.app_token for u in us]
    token = _random_str(TOKEN_LENGTH)
    while token in token_list:
        token = _random_str(TOKEN_LENGTH)
    at = AppToken(user_id=User.objects.get(user_id=user_id),
                  app_token=token,
                  ttl=datetime.now() + timedelta(days=TOKEN_TTL_DATE))
    at.save()
    return at


def _random_str(length, choice=''):
    """指定の長さのランダム英数文字列"""
    from random import choices
    import string
    if choice == '':
        choice = string.ascii_letters + string.digits
    return ''.join(choices(choice, k=length))
