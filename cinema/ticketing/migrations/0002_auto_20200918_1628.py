# Generated by Django 3.0.2 on 2020-09-18 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cinema_images/', verbose_name='تصویر'),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default='priority', upload_to='movie_poster/', verbose_name='پوستر'),
            preserve_default=False,
        ),
    ]