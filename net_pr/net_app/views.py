from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView
from .models import User, Post, CommentPost, Friend
from .forms import RegistrationForm, LoginForm, AddUserForm, CreatePostForm, UpdateUserForm,\
    AddCommentForPostForm, AddCommentForCommentForm, UpdatePostForm, UpdateCommentPostForm,\
    AddFriendForm, ApproveFriendForm
from django.db.models import Q

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
        # update_second_comment_form = UpdateSecondCommentPostForm()
    context = {
        'post_form': post_form,
        'comment_form': comment_form,
        'second_comment_form': second_comment_form,
        'update_post_form': update_post_form,
        'update_comment_form': update_comment_form,
        'profile': User.objects.filter(slug=slug),
        'posts': Post.objects.all().order_by('-date'),
        'comment': CommentPost.objects.filter(parent__isnull=True).order_by('-date'),
        'second_comment': CommentPost.objects.filter(parent__isnull=False).order_by('-date')
    }
    return render(request, 'user/profile.html', context)


def friends_list(request):
    approve_friend_form = ApproveFriendForm()
    if request.method == 'POST' and request.POST.get('submit') == 'approve_friend_form':
        person = request.POST.get('id')
        this_friend = get_object_or_404(Friend, id=person)
        approve_friend_form = AddFriendForm(data=request.POST, instance=this_friend)
        print(person, this_friend, request.POST)
        if approve_friend_form.is_valid():
            approve_friend_form.save(commit=False)
            approve_friend_form.approve_friendship = request.POST.get('approve_friendship')
            approve_friend_form.save()
            print(person, this_friend, request.POST)
            return redirect('friends')
    if request.method == 'POST' and request.POST.get('submit') == 'delete_friend_form':
        this_friend = int(request.POST.get('id'))
        Friend.objects.filter(pk=this_friend).delete()
        return redirect('friends')
    context = {
        'approve_friend_form': approve_friend_form,
        'user_list': User.objects.all(),
        'all_friends': Friend.objects.filter(approve_friendship=True),
        'not_approve_friends': Friend.objects.filter(name=request.user, approve_friendship=False),
        'my_request': Friend.objects.filter(friend=request.user, approve_friendship=False),
        'count_not_approve_friends': Friend.objects.filter(friend=request.user, approve_friendship=False).annotate\
            (count_not_approve_friends=Count('approve_friendship')).values_list('count_not_approve_friends', flat=True),
        'count_all_friends': Friend.objects.filter(Q(name=request.user) | Q(friend=request.user)).filter\
            (approve_friendship=True).annotate(count_all_friends=Count('approve_friendship')).values_list('count_all_friends', flat=True),
        'count_my_request': Friend.objects.filter(name=request.user, approve_friendship=False).annotate \
            (count_my_request=Count('approve_friendship')).values_list('count_my_request', flat=True),
    }
    return render(request, 'user/friends_list.html', context)


def users_list(request):
    add_friend_form = AddFriendForm()
    if request.method == 'POST' and request.POST.get('submit') == 'add_friend_form':
        person = request.POST.get('friend')
        this_friend = User.objects.get(slug=person)
        add_friend_form = AddFriendForm(data=request.POST)
        if add_friend_form.is_valid():
            add_friend_form.save(commit=False)
            add_friend_form.instance.name = request.user
            add_friend_form.instance.friend = this_friend
            add_friend_form.save()
            return redirect('all')
    if request.method == 'POST' and request.POST.get('submit') == 'delete_friend_form':
        this_friend = int(request.POST.get('id'))
        Friend.objects.filter(pk=this_friend).delete()
        return redirect(reverse('profile', kwargs={'slug': request.user.slug}))
    context = {
        'add_friend_form': add_friend_form,
        'user_list': User.objects.all(),
        'friends': Friend.objects.filter(name=request.user),
    }
    return render(request, 'user/all_list.html', context)


