from django.forms import ModelForm, DateInput
from MOT.models import Sinhvien
from django.utils.translation import gettext_lazy as _

class ThemSinhVienForm(ModelForm):
    class Meta:
        model = Sinhvien
        fields = ["mssv", "hotensv", "ngaysinh", "sodienthoai", "malop", "phanquyen"]
        labels = {
            "mssv": _("Mã số sinh viên"),
            "hotensv": _("Họ tên sinh viên"),
            "ngaysinh": _("Ngày sinh"),
            "sodienthoai": _("Số điện thoại"),
            "malop": _("Mã lớp")
        }
        exclude = ["phanquyen"]
        widgets = {
            "ngaysinh": DateInput(attrs={'type': 'date'}),
            
        }