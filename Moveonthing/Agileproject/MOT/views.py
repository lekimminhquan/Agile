from django.shortcuts import get_object_or_404, redirect, render
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

def detailStudent(request,mssv):
     student = get_object_or_404(Sinhvien, mssv=mssv)
     data = {
        'mssv': student.mssv,
        'hotensv': student.hotensv,
        'ngaysinh': student.ngaysinh.strftime('%d-%m-%Y'),
        'sodienthoai': student.sodienthoai,
        'malop': student.malop.malop,
    }
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(data)
     return render(request, 'detailStudent.html', {'student': student})
    

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
            if mahp:
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
            else:
                message = "Vui lòng chọn môn học tương ứng."
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
       # Lấy mã ngành từ query parameters
        selected_department = request.GET.get('department')
        
        # Truy vấn các ngành học từ CSDL
        departments = Nganh.objects.all()
        
        # Nếu người dùng đã chọn mã ngành
        if selected_department:
            # Lọc danh sách các môn học dựa trên mã ngành đã chọn
            subjects = Hocphan.objects.filter(manganh=selected_department)
            
            # Lấy mã học phần từ query parameters
            mahp = request.GET.get('subject')
            
            if mahp:
                students = Sinhvien.objects.filter(diem__mahp=mahp, malop__manganh=selected_department)
                student_list = []
                for student in students:
                    diem = Diem.objects.filter(mssv=student.mssv, mahp=mahp).first()
                    # tenlop = diem.tenlophp
                    diem_gk = diem.diemgk if diem else 0
                    diem_ck = diem.diemck if diem else 0
                    diem_tong = round((diem_gk * 0.3) + (diem_ck * 0.7), 2)
                    student_list.append({
                        # 'tenlophp' : student.tenlop,
                        'mssv': student.mssv,
                        'hotensv': student.hotensv,
                        'malop': student.malop,
                        'diem_gk': diem_gk,
                        'diem_ck': diem_ck,
                        'diem_tong': diem_tong
                    })
                
                return render(request, 'studentPoint.html', {'departments': departments,'subjects': subjects, 'student_list': student_list, 'selected_subject': mahp, 'selected_department': selected_department})
            
            else:
                # Trường hợp không có mã học phần được chọn, hiển thị danh sách môn học của ngành đó
                return render(request, 'studentPoint.html', {'departments': departments,'subjects': subjects,'selected_department': selected_department})
        
        else:
            # Trường hợp không có mã ngành được chọn, hiển thị ô select-department và danh sách môn học trống
            subjects = []
            return render(request, 'studentPoint.html', {'departments': departments,'subjects': subjects})
    
def Xoadiemsinhvien(request,mssv_id,mahp_id):
    if request.method == "GET":
        diem = Diem.objects.get(mssv=mssv_id,mahp = mahp_id)
        diem.delete()
    return redirect('Studentpoint')