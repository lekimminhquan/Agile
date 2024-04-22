from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout

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
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage') # Replace 'home' with the name of your home page URL
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'login.html', {'error': 'Failed'})