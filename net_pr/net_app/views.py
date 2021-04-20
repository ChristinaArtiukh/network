import os
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView
from pytils.translit import slugify

from .models import User, Post
from .forms import RegistrationForm, LoginForm, AddUserForm, CreatePost


def home(request):
    context = {
        'post': Post.objects.all().order_by('-date'),
    }
    return render(request, 'home.html', context)


def user_logout(request):
    logout(request)
    return redirect('registration')


def registration(request):
    log_form = LoginForm
    reg_form = RegistrationForm
    if request.method == "POST" and request.POST.get('submit') == 'login':
        log_form = LoginForm(data=request.POST or None)
        if log_form.is_valid():
            user = log_form.get_user()
            login(request, user)
            return redirect('home')
    elif request.method == "POST" and request.POST.get('submit') == 'register':
        reg_form = RegistrationForm(request.POST or None)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            return redirect('add_profile')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        log_form = LoginForm()
        reg_form = RegistrationForm()
    return render(request, 'user/registration.html', {'log_form': log_form, 'reg_form':reg_form})


def add_profile(request):
    if request.method == 'POST':
        profile_form = AddUserForm(data=request.POST, files=request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save(commit=False)
            profile_form.photo = request.FILES['photo']
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = AddUserForm()
    return render(request, 'user/add_profile.html', {'profile_form':profile_form})


def profile(request, slug):
    if request.method == 'POST':
        post_form = CreatePost(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.image = request.FILES.getlist('image')
            post_form.instance.user_name = request.user
            print('request.user', request.user, post_form)
            post_form.save()
            print('request.user', request.user, post_form)
            return HttpResponseRedirect(request.path_info)
    else:
        post_form = CreatePost()
    context = {
        'post_form': post_form,
        'profile': User.objects.filter(username=request.user),
        'post': Post.objects.filter(user_name=request.user).order_by('-date'),
    }
    print('request.user', request.user, post_form)
    return render(request, 'user/profile.html', context)


class FriendsListView(ListView):
    model = User
    template_name = 'user/friends_list.html'
    context_object_name = 'friends'


