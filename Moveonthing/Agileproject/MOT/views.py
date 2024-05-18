from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from MOT.models import Taikhoan, Sinhvien, Lop, Diem, Hocphan, Nganh
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from MOT.form import ThemSinhVienForm

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
    form = ThemSinhVienForm()
    if (request.method == "POST"):
        phanQuyen = Taikhoan.objects.get(phanquyen="student")
        f = ThemSinhVienForm(request.POST)
        if (f.is_valid()):
            sinhVien = f.save(commit=False) 
            sinhVien.phanquyen = phanQuyen
            sinhVien.save()
            messages.add_message(request, messages.SUCCESS, "Thêm sinh viên thành công")
        else:
            return render(request, 'sinhvien.html', {'danh_sach_sinh_vien': danh_sach_sinh_vien, 'form': f})
    return render(request, 'sinhvien.html', {'danh_sach_sinh_vien': danh_sach_sinh_vien, 'form': form})

def XoaSinhVien(request):
    if request.method == "POST":
        mssv = request.POST['mssv']
        sinhVien = Sinhvien.objects.get(mssv=mssv)
        sinhVien.delete()
        messages.add_message(request, messages.SUCCESS, "Xoá sinh viên thành công")
    return redirect("Sinhvien")
    

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

def educationprogram(request):
    departments = Nganh.objects.filter().order_by('manganh')
    selected_major = request.GET.get('major')
    
    # các hocphan từ ngành chọn
    if selected_major:
        displayed_courses = Hocphan.objects.filter(manganh=selected_major)
    else:
        displayed_courses = Hocphan.objects.none()  # không có học phần hiển thị nếu không chọn ngành

    context = {
        'departments': departments,
        'selected_major': selected_major,
        'displayed_courses': displayed_courses,
    }
    
    return render(request,'educationprogram.html',context)
def select_subject(request):
    if request.method == 'POST':
        # Kiểm tra nếu request là từ form pop-up
        if 'popup_form' in request.POST:
            mssv = request.POST.get('mssv')
            diem_gk = float(request.POST.get('diem_gk'))
            diem_ck = float(request.POST.get('diem_ck'))
            diem_tong = float(request.POST.get('diem_tong'))
            mahp = request.POST.get('selected_subject')
            is_update = request.POST.get('is_update', 'false') == 'true'

            # Kiểm tra sinh viên tồn tại trong CSDL
            sinhvien = Sinhvien.objects.filter(mssv=mssv).first()
            if sinhvien:
                # Kiểm tra nếu đây là yêu cầu cập nhật
                if is_update:
                    # Cập nhật điểm cho sinh viên
                    diem = Diem.objects.filter(mssv=sinhvien, mahp_id=mahp).first()
                    if diem:
                        diem.diemgk = diem_gk
                        diem.diemck = diem_ck
                        diem.diemtong = diem_tong
                        diem.save()
                        message = "Cập nhật điểm SV thành công."
                    else:
                        message = "Không tìm thấy điểm của sinh viên để cập nhật."
                else:
                    # Kiểm tra xem sinh viên đã có điểm ở môn này chưa
                    if not Diem.objects.filter(mssv=sinhvien, mahp_id=mahp).exists():
                        # Thêm điểm mới vào CSDL
                        new_diem = Diem.objects.create(mssv=sinhvien, mahp_id=mahp, diemgk=diem_gk, diemck=diem_ck, diemtong = diem_tong)
                        message = "Thêm điểm SV thành công."
                    else:
                        message = "Sinh viên đã có điểm ở môn này."
            else:
                message = "Sinh viên không tồn tại."

            return JsonResponse({'message': message})

        else:
            # Xử lý dữ liệu từ form chính
            mahp = request.POST.get('subject')

            students = Sinhvien.objects.filter(diem__mahp=mahp)
            student_list = []
            for student in students:
                diem = Diem.objects.filter(mssv=student.mssv, mahp=mahp).first()
                diem_gk = diem.diemgk if diem else 0
                diem_ck = diem.diemck if diem else 0
                diem_tong = diem.diemtong
                student_list.append({
                    'mssv': student.mssv,
                    'hotensv': student.hotensv,
                    'malop': student.malop,
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
    
