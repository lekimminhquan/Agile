# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Diem(models.Model):
    mssv = models.OneToOneField('Sinhvien', models.DO_NOTHING, db_column='mssv', primary_key=True)
    mahp = models.ForeignKey('Hocphan', models.DO_NOTHING, db_column='mahp')
    diemgk = models.FloatField(blank=True, null=True)
    diemck = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diem'
        unique_together = (('mssv', 'mahp'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Giangvienhuongdan(models.Model):
    magv = models.CharField(primary_key=True, max_length=20)
    hotengv = models.CharField(max_length=100, blank=True, null=True)
    ngaysinh = models.DateField(blank=True, null=True)
    sodienthoai = models.IntegerField(blank=True, null=True)
    malop = models.ForeignKey('Lop', models.DO_NOTHING, db_column='malop', blank=True, null=True)
    phanquyen = models.ForeignKey('Taikhoan', models.DO_NOTHING, db_column='phanquyen', to_field='phanquyen', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'giangvienhuongdan'


class Hocphan(models.Model):
    mahp = models.CharField(primary_key=True, max_length=20)
    tenhp = models.CharField(max_length=100, blank=True, null=True)
    sotinchi = models.IntegerField(blank=True, null=True)
    manganh = models.ForeignKey('Nganh', models.DO_NOTHING, db_column='manganh', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hocphan'


class Lop(models.Model):
    malop = models.CharField(primary_key=True, max_length=20)
    tenlop = models.CharField(max_length=100, blank=True, null=True)
    manganh = models.ForeignKey('Nganh', models.DO_NOTHING, db_column='manganh', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lop'


class Nganh(models.Model):
    manganh = models.CharField(primary_key=True, max_length=20)
    tennganh = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nganh'


class Phonggiaovu(models.Model):
    mapgv = models.CharField(primary_key=True, max_length=20)
    tenphong = models.CharField(max_length=100, blank=True, null=True)
    phanquyen = models.ForeignKey('Taikhoan', models.DO_NOTHING, db_column='phanquyen', to_field='phanquyen', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phonggiaovu'


class Sinhvien(models.Model):
    mssv = models.CharField(primary_key=True, max_length=20)
    hotensv = models.CharField(max_length=100, blank=True, null=True)
    ngaysinh = models.DateField(blank=True, null=True)
    sodienthoai = models.IntegerField(blank=True, null=True)
    malop = models.ForeignKey(Lop, models.DO_NOTHING, db_column='malop', blank=True, null=True)
    phanquyen = models.ForeignKey('Taikhoan', models.DO_NOTHING, db_column='phanquyen', to_field='phanquyen', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sinhvien'


class Taikhoan(AbstractBaseUser):
    matk = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password =  models.CharField(max_length=50,blank=True, null=True)
    phanquyen = models.CharField(unique=True, max_length=20, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taikhoan'
