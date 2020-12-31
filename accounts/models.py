from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import main.models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedDateField, EncryptedTextField, EncryptedMixin

# Create your models here.
class EncryptedPhoneNumberField(EncryptedMixin, PhoneNumberField):
    pass

class User(AbstractUser):
    full_name = models.CharField(max_length=1000)

    # Get all posts liked by user
    @property
    def liked_posts(self):
        posts = []
        for post in main.models.Post.objects.all():
            if post.is_liked_by_user(self):
                posts.append(post.id)
        return posts
    
    # Set full_name field to user's full name upon sign up. For search purposes.
    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()

        super(User, self).save(*args, **kwargs)


# class Interest(models.Model):
#     CHOICES = [
#         ('music' ,  "Music"),
#         ('photography' , "Photography"),
#         ('acting' , "Acting"),
#         ('art' , "Art"),
#         ('travel' , "Travel"),
#         ('sports' , "Sports"),
#         ('dance'  , "Dance"),
#         ('architectures' , "Architectures"),
#         ('humanity' , "Humanity"),
#         ('food' , "Food"),
#         ('fashion' , "Fashion"),
#         ('cricket' , "Cricket"),
#         ('comedy' , "comedy"),
#         ('education' , "Education"),
#         ('poetry' , "Poetry"),
#         ('spiritual' , "Spiritual"),
#         ('fitness' , "Fitness"),
#         ('auto' , "Auto/Moto")
# ]
#     interests = MultiSelectField(choices=CHOICES)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = EncryptedTextField()
    phone_number = EncryptedPhoneNumberField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDERS, default='------')
    date_of_birth = EncryptedDateField(null=True, blank=True)
    # interests = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    website = models.URLField(default='', blank=True)
    bio = models.CharField(max_length=170, default="", blank=True)
    verified = models.BooleanField(default=False)
    notification_count = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user_id", "following_user_id"]]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


# Create New Profile on Sign Up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
