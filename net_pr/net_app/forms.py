from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Post, CommentPost
from django.utils.translation import gettext_lazy as gl


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'register-form-username': gl('Логин'),
            'login-form-email': gl('Почта'),
            'password1': gl('Пароль'),
            'password2': gl('Подтверждение пароля'),
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        # exclude = ('__all__',)
        fields = ('first_name', 'last_name', 'photo', 'bio', 'sex', 'b_day')
        exclude = ('password', 'slug')


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo', 'bio', 'b_day')
        exclude = ('password', 'sex', 'slug')


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')
        exclude = ('url', 'video', 'music', 'name')


class AddCommentForPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('comment', 'post',)
        exclude = ('name', 'poster')


class AddCommentForCommentForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('post', 'parent', 'comment', )
        exclude = ('name', )


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')


class UpdateCommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('comment', )


class UpdateSecondCommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('comment', )