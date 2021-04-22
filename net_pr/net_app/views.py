import os
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView
from pytils.translit import slugify

from .models import User, Post, CommentPost
from .forms import RegistrationForm, LoginForm, AddUserForm, CreatePostForm, UpdateUserForm,\
    AddCommentForPostForm


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
    return render(request, 'user/add_profile.html', {'profile_form': profile_form})


def profile(request, slug):
    post_form = CreatePostForm()
    comment_form = AddCommentForPostForm()
    if request.method == 'POST' and request.POST.get('submit') == 'post_form':
        post_form = CreatePostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.instance.name = request.user
            post_form.save()
            return HttpResponseRedirect(request.path_info)
    elif request.method == 'POST' and request.POST.get('submit') == 'comment_form':
        comment_form = AddCommentForPostForm(data=request.POST)
        this_post = int(request.POST.get('post'))
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.instance.name = request.user
            comment_form.post = Post.objects.filter(pk=this_post)
            comment_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        post_form = CreatePostForm()
        comment_form = AddCommentForPostForm()
    context = {
        'post_form': post_form,
        'comment_form': comment_form,
        'profile': User.objects.filter(slug=slug),
        'posts': Post.objects.all().order_by('-date'),
        'comment': CommentPost.objects.all().order_by('-date')
    }
    return render(request, 'user/profile.html', context)


class FriendsListView(ListView):
    model = User
    template_name = 'user/friends_list.html'
    context_object_name = 'friends'


class UpdateUserInfo(UpdateView):
    model = User
    template_name = 'user/update_user.html'
    success_url = 'profile'
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        return self.request.user

