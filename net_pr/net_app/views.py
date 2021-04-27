from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView
from .models import User, Post, CommentPost
from .forms import RegistrationForm, LoginForm, AddUserForm, CreatePostForm, UpdateUserForm,\
    AddCommentForPostForm, AddCommentForCommentForm, UpdatePostForm, UpdateCommentPostForm,\
    UpdateSecondCommentPostForm


def home(request):
    context = {
        'post': Post.objects.all().order_by('-date'),
    }
    return render(request, 'home.html', context)


def user_logout(request):
    '''
    выход из учетки пользователя
    '''
    logout(request)
    return redirect('registration')


def registration(request):
    '''
    Регистрация пользователя
    '''
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
    '''
    Добавление данных к пользователю
    '''
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


class UpdateUserInfo(UpdateView):
    '''
    Редактированик данных пользователя
    '''
    model = User
    template_name = 'user/update_user.html'
    success_url = 'profile'
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        return self.request.user


def profile(request, slug):
    '''
    Страница пользователя:
    CreatePostForm() - добавление поста на страницу
    AddCommentForPostForm() - добавление комментария к посту
    AddCommentForCommentForm() - добавление комментария к комментарию
    UpdatePostForm() - редактирование поста
    UpdateCommentPostForm() - редактирование комментария

    '''
    post_form = CreatePostForm()
    comment_form = AddCommentForPostForm()
    second_comment_form = AddCommentForCommentForm()
    update_post_form = UpdatePostForm()
    update_comment_form = UpdateCommentPostForm()
    update_second_comment_form = UpdateSecondCommentPostForm()
    this_name = User.objects.get(slug=slug)
    # добавление поста на страницу
    if request.method == 'POST' and request.POST.get('submit') == 'post_form':
        post_form = CreatePostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.instance.poster = request.user
            post_form.instance.name = this_name
            post_form.save()
            return HttpResponseRedirect(request.path_info)
    #  добавление комментария к посту
    elif request.method == 'POST' and request.POST.get('submit') == 'comment_form':
        comment_form = AddCommentForPostForm(data=request.POST)
        this_post = int(request.POST.get('post'))
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.instance.poster = request.user
            comment_form.instance.name = this_name
            comment_form.post = Post.objects.filter(pk=this_post)
            comment_form.save()
            return HttpResponseRedirect(request.path_info)
    # добавление комментария к комментарию
    elif request.method == 'POST' and request.POST.get('submit') == 'second_comment_form':
        second_comment_form = AddCommentForCommentForm(data=request.POST)
        this_post = int(request.POST.get('post'))
        this_comment = int(request.POST.get('parent'))
        if second_comment_form.is_valid():
            second_comment_form.save(commit=False)
            second_comment_form.instance.poster = request.user
            second_comment_form.post = Post.objects.filter(pk=this_post)
            second_comment_form.parent = this_comment
            second_comment_form.instance.name = this_name
            second_comment_form.save()
            return HttpResponseRedirect(request.path_info)
    # редактирование поста
    elif request.method == 'POST' and request.POST.get('submit') == 'update_post_form':
        this_post = int(request.POST.get('post'))
        instance = get_object_or_404(Post, pk=this_post)
        update_post_form = UpdatePostForm(data=request.POST, instance=instance, files=request.FILES)
        if update_post_form.is_valid():
            update_post_form.save()
            print(instance, request.POST)
            return HttpResponseRedirect(request.path_info)
    # редактирование комментария
    elif request.method == 'POST' and request.POST.get('submit') == 'update_comment_form' \
            or request.POST.get('submit') == 'update_second_comment_form':
        this_comment = request.POST.get('id')
        instance = get_object_or_404(CommentPost, pk=this_comment)
        update_comment_form = UpdateCommentPostForm(data=request.POST, instance=instance)
        print(instance, request.POST)
        if update_comment_form.is_valid():
            update_comment_form.save()
            print(instance, this_comment, request.POST)
            return HttpResponseRedirect(request.path_info)
    # редактирование комментария на комментарий
    elif request.method == 'POST' and request.POST.get('submit') == 'update_second_comment_form':
        this_comment = request.POST.get('id')
        instance = get_object_or_404(CommentPost, pk=this_comment, )
        update_second_comment_form = UpdateSecondCommentPostForm(data=request.POST, instance=instance)
        print(instance, request.POST)
        if update_second_comment_form.is_valid():
            update_second_comment_form.save()
            print(instance, this_comment, request.POST)
            return HttpResponseRedirect(request.path_info)
    # удаление поста
    elif request.method == 'POST' and request.POST.get('submit') == 'delete_post_form':
        this_post = int(request.POST.get('post'))
        Post.objects.filter(pk=this_post).delete()
        return HttpResponseRedirect(request.path_info)
    # удаление родительского и дочернего комментария
    elif request.method == 'POST' and request.POST.get('submit') == 'delete_comment_form'\
            or request.POST.get('submit') == 'delete_second_comment_form':
        this_comment = int(request.POST.get('comment'))
        CommentPost.objects.filter(pk=this_comment).delete()
        return HttpResponseRedirect(request.path_info)
    else:
        post_form = CreatePostForm()
        comment_form = AddCommentForPostForm()
        second_comment_form = AddCommentForPostForm()
        update_post_form = UpdatePostForm()
        update_comment_form = UpdateCommentPostForm()
        update_second_comment_form = UpdateSecondCommentPostForm()
    context = {
        'post_form': post_form,
        'comment_form': comment_form,
        'second_comment_form': second_comment_form,
        'update_post_form': update_post_form,
        'update_comment_form': update_comment_form,
        'update_second_comment_form': update_second_comment_form,
        'profile': User.objects.filter(slug=slug),
        'posts': Post.objects.all().order_by('-date'),
        'comment': CommentPost.objects.filter(parent__isnull=True).order_by('-date'),
        'second_comment': CommentPost.objects.filter(parent__isnull=False).order_by('-date')
    }
    return render(request, 'user/profile.html', context)


class FriendsListView(ListView):
    model = User
    template_name = 'user/friends_list.html'
    context_object_name = 'friends'




