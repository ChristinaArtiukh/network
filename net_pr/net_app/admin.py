from django.contrib import admin
from .models import User, Post, CommentPost, Friends, OneOnOneRoom, Chat

admin.site.register(User)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(Friends)
admin.site.register(OneOnOneRoom)
admin.site.register(Chat)
