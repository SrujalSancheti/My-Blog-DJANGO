from django.contrib import admin
from django.urls import path,include
from Home import views

urlpatterns = [
    path('', views.home , name = "home"),   
    path('contact', views.contact , name = "contact"),
    path('about/', views.about , name = "about"),
    path('search', views.search , name = "search"),
    path('signup', views.handleSignUp , name = "handleSignUp"),
    path('login', views.handlelogin , name = "handlelogin"),
    path('logout', views.handlelogout , name = "handlelogout"),
 
]