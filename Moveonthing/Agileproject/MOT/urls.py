from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Agile, name= 'Agile'),
    path('forgot',views.Forgot, name='Forgot'),
    path('login', views.Login, name= 'Login'),
    path('homepage', views.Homepage, name='Homepage')
]
