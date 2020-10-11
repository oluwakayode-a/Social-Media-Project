from django import template
from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()

@register.simple_tag
def is_following(user, target_id):
    following_ids = [x.following_user_id.id for x in user.following.all()]
    
    # get all users followed by logged in user, and check if target user exists there.
    user_exists = User.objects.filter(id__in=following_ids).filter(id=target_id).exists()
    return user_exists
   
