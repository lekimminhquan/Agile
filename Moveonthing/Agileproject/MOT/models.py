from django.db import models

class Sinhvien(models.Model):
    IDSV =models.AutoField(primary_key=True)
    TEN =models.CharField(max_length =100)
    NGAYSINH =models.DateTimeField(null = False)
    DIEM = models.IntegerField(blank = True,null =True)