from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from accounts.models import Profile
from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required


User = get_user_model()
# Create your views here.

@login_required
def index(request):
    profiles = Profile.objects.exclude(user=request.user)
    posts = Post.objects.all()

    context = {
        'profiles' : profiles,
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
        print('comment added')

        return redirect('main:index')


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

    return redirect('main:index')

