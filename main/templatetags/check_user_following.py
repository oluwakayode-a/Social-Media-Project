from django import template

register = template.Library()

@register.simple_tag
def is_following(user, following_user_id):
    for i in user.following.all():
        if following_user_id == i:
            return True
        return False
