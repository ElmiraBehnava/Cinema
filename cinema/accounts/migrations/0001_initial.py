# Generated by Django 3.0.2 on 2020-09-21 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='تلفن همراه')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='users/profile_images/', verbose_name='تصویر')),
                ('gender', models.IntegerField(choices=[(1, 'مرد'), (2, 'زن')], verbose_name='جنسیت')),
                ('balance', models.IntegerField(default=0, verbose_name='اعتبار')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='حساب کاربری')),
            ],
        ),
    ]