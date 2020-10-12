from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, UserFollowing, Interest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import ProfileForm, InterestForm
from main.models import Notification, Post

User = get_user_model()

# Create your views here.
def users_list(request):
    if request.user.is_authenticated:
        users = Profile.objects.exclude(request.user)
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

    # create new notification
    new_notification = Notification.objects.create(
        user=user_to_follow,
        notification_type='user-plus',
        text=f'{request.user.get_full_name()} followed you'
    )
    new_notification.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, target_id):
    # To unfollow, simply delete the following entry
    get_following = UserFollowing.objects.get(user_id=request.user.id, following_user_id=target_id)
    get_following.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)

    context = {
        'profile' : user_profile,
        'posts' : posts
    }
    return render(request, 'accounts/photo_profile.html', context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

        return redirect('main:index')
    context = {
        'form' : form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def edit_interests(request):
    form = InterestForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/edit_profile')
        # add interests to logged in user.
    else:
        print(form.errors)
    context = {
        'form' : form
    }
    return render(request, 'accounts/interests.html', context)


@login_required
def followers(request):
    # isolate all user ids of users following currently logged in user
    excluded = [user.user_id.id for user in request.user.followers.all()]

    # list all users following logged in user.
    followers = User.objects.filter(id__in=excluded).exclude(username=request.user.username)
    context = {
        'followers' : followers
    }
    return render(request, 'accounts/photo_followers.html', context)


@login_required
def following(request):
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list all users followed by logged in user.
    following = User.objects.filter(id__in=excluded).exclude(username=request.user.username)
    context = {
        'following' : following
    }
    return render(request, 'accounts/photo_following.html', context)


    



    
