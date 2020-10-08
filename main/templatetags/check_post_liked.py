from django import template

register = template.Library()

@register.filter(name="has_liked")
def is_liked(post, user):
    return post.likes.filter(user=user).exists()

