from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

category_choices = [
        ('music' ,  "Music"),
        ('photography' , "Photography"),
        ('acting' , "Acting"),
        ('art' , "Art"),
        ('travel' , "Travel"),
        ('sports' , "Sports"),
        ('dance'  , "Dance"),
        ('architectures' , "Architectures"),
        ('humanity' , "Humanity"),
        ('food' , "Food"),
        ('fashion' , "Fashion"),
        ('cricket' , "Cricket"),
        ('comedy' , "comedy"),
        ('education' , "Education"),
        ('poetry' , "Poetry"),
        ('spiritual' , "Spiritual"),
        ('fitness' , "Fitness"),
        ('auto' , "Auto/Moto")
]


class Post(models.Model):
    caption = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # category = models.CharField(max_length=20, choices= category_choices, default="select option")

    def __str__(self):
        return self.caption
    

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
    
