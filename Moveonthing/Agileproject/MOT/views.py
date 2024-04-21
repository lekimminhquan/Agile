from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def Agile (request):
    template = loader.get_template('agile.html')
    return HttpResponse(template.render())

def Forgot(request):
    template = loader.get_template('forgotPassword.html')
    return HttpResponse(template.render())

def Login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def Homepage(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())
def Resetpass(request):
    template = loader.get_template('resetPassword.html')
    return HttpResponse(template.render())
