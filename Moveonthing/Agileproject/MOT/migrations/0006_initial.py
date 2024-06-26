# Generated by Django 4.1.13 on 2024-04-21 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Giangvienhuongdan',
            fields=[
                ('magv', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('hotengv', models.CharField(blank=True, max_length=100, null=True)),
                ('ngaysinh', models.DateField(blank=True, null=True)),
                ('sodienthoai', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'giangvienhuongdan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Hocphan',
            fields=[
                ('mahp', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tenhp', models.CharField(blank=True, max_length=100, null=True)),
                ('sotinchi', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hocphan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lop',
            fields=[
                ('malop', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tenlop', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'lop',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nganh',
            fields=[
                ('manganh', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tennganh', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'nganh',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Phonggiaovu',
            fields=[
                ('mapgv', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tenphong', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'phonggiaovu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sinhvien',
            fields=[
                ('mssv', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('hotensv', models.CharField(blank=True, max_length=100, null=True)),
                ('ngaysinh', models.DateField(blank=True, null=True)),
                ('sodienthoai', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sinhvien',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Taikhoan',
            fields=[
                ('matk', models.AutoField(primary_key=True, serialize=False)),
                ('tendangnhap', models.CharField(blank=True, max_length=50, null=True)),
                ('matkhau', models.CharField(blank=True, max_length=50, null=True)),
                ('phanquyen', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
            options={
                'db_table': 'taikhoan',
                'managed': False,
            },
        ),
    ]
