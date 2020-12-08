from django.contrib import admin
from .models import Post, Like, Comment, Notification, Suggestion

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Suggestion)