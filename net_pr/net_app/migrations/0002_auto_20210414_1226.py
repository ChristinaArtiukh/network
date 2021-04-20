# Generated by Django 3.2 on 2021-04-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='b_day',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Краткая информация'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media//%Y/%m/%d', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('men', 'Мужчина'), ('women', 'Женщина')], max_length=30, null=True, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='Ссылка'),
        ),
    ]