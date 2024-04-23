from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Agile, name= 'Agile'),
    path('forgot',views.Forgot, name='Forgot'),
    path('reset',views.Resetpass, name='Reset'),
    path('login', views.Login, name= 'Login'),
    path('logout', views.Login, name= 'Logout'),
    path('homepage', views.Homepage, name='Homepage'),
]
