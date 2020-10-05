from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website = models.URLField(default='www.earthruh.com')
    bio = models.CharField(max_length=170, default="Input Bio Here.")
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


# Create New Profile on Sign Up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
