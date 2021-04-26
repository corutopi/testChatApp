from django.shortcuts import render

from django.http import HttpResponse


def login(request):
    return HttpResponse('Login View')


def mypage(request):
    return HttpResponse('MyPage View')


def register(request):
    return HttpResponse('Register View')
