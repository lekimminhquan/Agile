from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from MOT.models import Taikhoan

def Agile (request):
    template = loader.get_template('agile.html')
    return HttpResponse(template.render())

def Forgot(request):
    template = loader.get_template('forgotPassword.html')
    return HttpResponse(template.render())
@login_required(login_url='/login')
def Homepage(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def Resetpass(request):
    template = loader.get_template('resetPassword.html')
    return HttpResponse(template.render())

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['checka']
        user = authenticate(username=username, password=password, role=role)
        if user is not None:
            login(request, user)
            return redirect('Homepage') 
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def Logout(request):
    logout(request)
    return redirect('Agile')