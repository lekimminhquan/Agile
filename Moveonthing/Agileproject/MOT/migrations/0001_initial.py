# Generated by Django 4.1.13 on 2024-03-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sinhvien',
            fields=[
                ('IDSV', models.AutoField(primary_key=True, serialize=False)),
                ('TEN', models.CharField(max_length=100)),
                ('NGAYSINH', models.DateTimeField()),
                ('DIEM', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
