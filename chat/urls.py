from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.login, name='default'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('registered/', views.registered, name='registered'),
    path('mypage/', views.mypage, name='mypage'),
    path('logout/', views.logout, name='logout'),
    path('loggedout/', views.loggedout, name='loggedout'),
]
