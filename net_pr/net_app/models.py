from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class User(AbstractUser):
    SEX_CHOICE = (
                ('men', 'Мужчина'),
                ('women', 'Женщина'),
            )
    date_join = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    phone = models.CharField(max_length=13, verbose_name='Телефон')
    photo = models.ImageField(upload_to='media/user/%Y/%m/%d', verbose_name='Фото', blank=True, null=True)
    bio = models.TextField(verbose_name='Краткая информация', blank=True, null=True)
    sex = models.CharField(choices=SEX_CHOICE, max_length=30, verbose_name='Пол', null=True)
    b_day = models.DateField(verbose_name='Дата рождения', null=True)
    slug = models.SlugField(verbose_name='Ссылка', unique=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Post(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/post/%Y/%m/%d', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='media/post/%Y/%m/%d', blank=True, null=True)
    music = models.FileField(upload_to='media/post/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


