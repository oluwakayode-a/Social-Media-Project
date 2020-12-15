from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    CATEGORIES = [
        ('art', 'Art'),
        ('photography', 'Photography')
    ]
    caption = models.CharField(max_length=500, blank=True, null=True)
    event = models.BooleanField(default=False)
    event_url = models.CharField(max_length=100, blank=True, null=True)
    venue = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="art")

    def __str__(self):
        return f"post-{self.id}"
    

    @property
    def like_count(self):
        return self.likes.all().count()
    
    @property
    def comment_count(self):
        return self.comments.all().count()
    
    def is_liked_by_user(self, user):
        return True if self.likes.filter(user=user).exists() else False



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s comment on {self.post.caption[:50]}'"


class Notification(models.Model):
    CHOICES = [
        ('comment', 'Comment'),
        ('plus', 'Like'),
        ('user-plus', 'Follow')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="triggered_by")
    notification_type = models.CharField(max_length=10, choices=CHOICES)
    text = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created']

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    text = models.TextField()

    def __str__(self):
        return f"Suggestion by @{self.user.username}"


class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.post} by {self.user}"
    