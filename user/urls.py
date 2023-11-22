from django.urls import path
from . import views

urlpatterns =[
    path('api/login/', views.login_view),#
    path('signout/', views.singout,name='signout'),
    path('signin/', views.signin,name='signin'),
    path('register/', views.register, name='register'),
    path('api/login/', views.login_view),
    path('home/', views.home,name='home'),
    path('help/', views.help,name='help'),
    path('', views.home,name='home'),
]