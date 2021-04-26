from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='default'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('mypage', views.mypage, name='mypage')
]
