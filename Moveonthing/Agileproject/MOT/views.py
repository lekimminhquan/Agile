from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from MOT.models import Taikhoan, Sinhvien, Lop
from django.contrib.auth.hashers import make_password

def Agile (request):
    template = loader.get_template('agile.html')
    return HttpResponse(template.render())

def Forgot(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        user_exists = Taikhoan.objects.filter(username=username).exists()
        if user_exists:
            request.session['reset_username'] = username
            return redirect('Reset')
        else:
            messages.error(request, "Username does not exist.")  
            return render(request, 'forgotPassword.html')
    else:
        return render(request, 'forgotPassword.html')

@login_required(login_url='/login')
def Homepage(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def Resetpass(request):
    if request.method == 'POST':
        username = request.session.get('reset_username', '').strip()
        new_password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm-pw', '').strip()
        if len(new_password) > 50:
            messages.error(request, "Password is too long")
            return render(request, 'resetPassword.html')
        if new_password != confirm_password:
            messages.error(request, "Password doesn't match")
            return render(request, 'resetPassword.html')
        if not username:
            messages.error(request, "Username doesn't exist, input again")
            return redirect('ForgotPassword')
        try:
            user = Taikhoan.objects.get(username=username)
            user.password = new_password 
            user.save()
            del request.session['reset_username']
            messages.success(request, "Updated password")
            return redirect('Login') 
        except Taikhoan.DoesNotExist:
            messages.error(request, "Username doesn't exist")
            return render(request, 'resetPassword.html')

    else:
        return render(request, 'resetPassword.html')

def Login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['checka']
        user = authenticate(username=username, password=password, role=role)
        if user is not None:
            login(request, user)
            return redirect('Homepage') 
        else:
            messages.warning(request, "Tài khoản hoặc mật khẩu không đúng. Vui lòng thử lại")
            context["username"] = username
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('Login')

def TrangSinhvien(request):
    if request.method == 'POST':
        mssv = request.POST['mssv']
        hotensv = request.POST['hotensv']
        ngaysinh = request.POST['ngaysinh']
        sodienthoai = request.POST['sodienthoai']
        malop = Lop.objects.get(malop="K47.CNTT")
        phanquyen = Taikhoan.objects.get(phanquyen="student")
        sinhvien = Sinhvien.objects.create(mssv=mssv, hotensv=hotensv, ngaysinh=ngaysinh, sodienthoai=sodienthoai, malop=malop, phanquyen=phanquyen)
    return render(request, 'sinhvien.html')