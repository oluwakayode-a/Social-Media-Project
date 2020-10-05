from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Profile, UserFollowing
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def users_list(request):
    if request.user.is_authenticated:
        users = Profile.objects.exclude(user=request.user)
    else:
        users = Profile.objects.all()
    context = {
        'users' : users
    }

    return HttpResponse(context)

@login_required
def follow(request, target_id):
    user_to_follow = User.objects.get(id=target_id)
    new_follow = UserFollowing.objects.create(
        user_id=request.user,
        following_user_id=user_to_follow
    )
    new_follow.save()

    return HttpResponse('successful')


@login_required
def unfollow(request, target_id):
    user_to_unfollow = User.objects.get(id=target_id)
    new_follow = get_object_or_404(UserFollowing, following_user_id=user_to_unfollow)
    new_follow.delete()

    return HttpResponse('successful')
    
    



    
