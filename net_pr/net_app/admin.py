from django.contrib import admin
from .models import User, Post, CommentPost

admin.site.register(User)
admin.site.register(Post)
admin.site.register(CommentPost)
