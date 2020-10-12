from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from accounts.models import Profile, UserFollowing
from .models import Post, Like, Comment, Notification
from django.contrib.auth.decorators import login_required


User = get_user_model()
# Create your views here.

@login_required
def index(request):
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list all users not followed by logged in user.
    suggested = User.objects.exclude(id__in=excluded).exclude(username=request.user.username)
    
    posts = Post.objects.all()

    context = {
        'suggested' : suggested,
        'posts' : posts,
    }
    return render(request, 'main/photo_home.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        post_id = request.POST['post_id']

        post = Post.objects.get(id=post_id)

        new_comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=comment_text
        )
        new_comment.save()
        
        # create notification for all users except logged in user
        users = User.objects.exclude(username=request.user.username)
        for user in users:
            new_notification = Notification.objects.create(
                user=user,
                text=f"{request.user.get_full_name()} commented on {post.user.get_full_name()}'s post",
                notification_type='comment'
            )
            new_notification.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_toggle(request, post_id):
    post = Post.objects.get(id=post_id)
    # check if user has liked post
    if post.is_liked_by_user(request.user):
        # remove the like
        Like.objects.get(post=post, user=request.user).delete()
    else:
        new_like = Like.objects.create(
            post=post,
            user=request.user
        )
        new_like.save()

         # create new notification
        new_notification = Notification.objects.create(
            user=post.user,
            notification_type='heart',
            text=f'{request.user.get_full_name()} liked your post'
        )
        new_notification.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def upload(request):
    if request.method == 'POST':
        caption = request.POST['caption']
        image = request.FILES['file-input']

        new_post = Post.objects.create(
            caption=caption,
            image=image,
            user=request.user
        )
        new_post.save()

        return redirect('main:index')
    return render(request, 'main/photo_upload.html')


@login_required
def explore(request):
    posts = Post.objects.all()
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list all users not followed by logged in user.
    suggested = User.objects.exclude(id__in=excluded).exclude(username=request.user.username)

    context = {
        'posts' : posts,
        'suggested' : suggested
    }

    return render(request, 'main/photo_explore.html', context)
