from django.contrib import admin
from .models import Post, Like, Comment, Notification, Suggestion, Report, Inquiry

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    search_fields = ['id', 'caption']

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Suggestion)
admin.site.register(Report)
admin.site.register(Inquiry)