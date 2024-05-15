from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from MOT.models import Taikhoan, Sinhvien, Lop, Diem, Hocphan, Nganh
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


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
    if request.user.is_authenticated:
        return redirect('Homepage')
    if request.method == 'POST':
        context = {}
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
    danh_sach_sinh_vien = Sinhvien.objects.all()
    if request.method == 'POST':
        mssv = request.POST["mssv"]
        hotensv = request.POST["hotensv"]
        ngaysinh = request.POST["ngaysinh"]
        sodienthoai = request.POST["sodienthoai"]
        malop = Lop.objects.get(malop="K47.CNTT")
        phanquyen = Taikhoan.objects.get(phanquyen="student")
        sinhvien = Sinhvien.objects.create(mssv=mssv, hotensv=hotensv, ngaysinh=ngaysinh, sodienthoai=sodienthoai, malop=malop, phanquyen=phanquyen)       
    return render(request, 'sinhvien.html', {'danh_sach_sinh_vien': danh_sach_sinh_vien})

def searchSinhVien(request):
    query = request.GET.get('query', '')
    sinh_vien_list = Sinhvien.objects.filter(
        mssv__icontains=query
    )|Sinhvien.objects.filter(hotensv__icontains=query)
    data = [{
        'mssv': sv.mssv,
        'hotensv': sv.hotensv,
        'ngaysinh': sv.ngaysinh.strftime('%Y-%m-%d'),
        'sodienthoai': sv.sodienthoai,
        'malop':sv.malop.malop
    }  for sv in sinh_vien_list]

    return JsonResponse(data, safe=False)

def select_subject(request):
    if request.method == 'POST':
        # Kiểm tra nếu request là từ form pop-up
        if 'popup_form' in request.POST:
            mssv = request.POST.get('mssv')
            diem_gk = float(request.POST.get('diem_gk'))
            diem_ck = float(request.POST.get('diem_ck'))
            mahp = request.POST.get('selected_subject')

            # Kiểm tra sinh viên tồn tại trong CSDL
            sinhvien = Sinhvien.objects.filter(mssv=mssv).first()
            if sinhvien:
                # Kiểm tra xem sinh viên đã có điểm ở môn này chưa
                if not Diem.objects.filter(mssv=sinhvien, mahp_id=mahp).exists():
                    # Thêm điểm mới vào CSDL
                    new_diem = Diem.objects.create(mssv=sinhvien, mahp_id=mahp, diemgk=diem_gk, diemck=diem_ck)
                    message = "Thêm điểm SV thành công."
                else:
                    message = "Sinh viên đã có điểm ở môn này."
            else:
                message = "Sinh viên không tồn tại."

            return JsonResponse({'message': message})

        else:
                    # Xử lý dữ liệu từ form chính
                    # Lấy mã học phần từ form
                    mahp = request.POST.get('subject')

                    students = Sinhvien.objects.filter(diem__mahp=mahp)
                    student_list = []
                    for student in students:
                        diem = Diem.objects.filter(mssv=student.mssv, mahp=mahp).first()
                        diem_gk = diem.diemgk if diem else 0
                        diem_ck = diem.diemck if diem else 0
                        diem_tong = round((diem_gk * 0.3) + (diem_ck * 0.7), 2)
                        student_list.append({
                            'mssv': student.mssv,
                            'hotensv': student.hotensv,
                            'tenlop': student.malop.tenlop,
                            'diem_gk': diem_gk,
                            'diem_ck': diem_ck,
                            'diem_tong': diem_tong
                        })
                    subjects = Hocphan.objects.all()
                    return render(request, 'studentPoint.html', {'subjects': subjects, 'student_list': student_list, 'selected_subject': mahp})

    else:
        # Nếu là GET request, chỉ hiển thị form chọn môn học
        subjects = Hocphan.objects.all()
        return render(request, 'studentPoint.html', {'subjects': subjects})
    
