from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

category_choices = {
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
    }


class Post(models.Model):
    caption = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices= category_choices, default="select option")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    
