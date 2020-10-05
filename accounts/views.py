from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Profile, UserFollowing
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import ProfileForm

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
def unfollow(request, follow_id):
    # To unfollow, simply delete the following entry
    get_following = UserFollowing.objects.get(id=follow_id)
    get_following.delete()

    return HttpResponse('successful')


@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)

    context = {
        'profile' : user_profile
    }
    return render(request, 'accounts/photo_profile.html', context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

        return redirect('/profile')
    context = {
        'form' : form
    }
    return render(request, 'accounts/edit_profile.html', context)

    



    
