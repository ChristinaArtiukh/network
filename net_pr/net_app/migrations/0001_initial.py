# Generated by Django 3.2 on 2021-05-20 12:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_join', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='Телефон')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/user/%Y/%m/%d', verbose_name='Фото')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Краткая информация')),
                ('sex', models.CharField(choices=[('men', 'Мужчина'), ('women', 'Женщина')], max_length=30, null=True, verbose_name='Пол')),
                ('b_day', models.DateField(null=True, verbose_name='Дата рождения')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='Ссылка')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/post/%Y/%m/%d')),
                ('url', models.URLField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='media/post/%Y/%m/%d')),
                ('music', models.FileField(blank=True, null=True, upload_to='media/post/%Y/%m/%d')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='OneOnOneRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.SlugField(null=True, unique=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_sender', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('approve_friendship', models.BooleanField(default=False)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_friend', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_friend', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Друг',
                'verbose_name_plural': 'Друзья',
            },
        ),
        migrations.CreateModel(
            name='CommentPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='Комментарий')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='net_app.commentpost')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_app.post')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_poster', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Коментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('room_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_app.oneononeroom')),
            ],
        ),
    ]
