from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile, UserFollowing
from django.db.models import Q, Count
from .models import Post, Like, Comment, Notification
from .forms import SuggestionForm, ReportForm
from django.contrib.auth.decorators import login_required
import json


User = get_user_model()
# Create your views here.

@login_required
def index(request):
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list all users not followed by logged in user.
    suggested = User.objects.exclude(id__in=excluded).exclude(username=request.user.username)
    
    posts = Post.objects.all().order_by('-created')

    context = {
        'suggested' : suggested,
        'posts' : posts,
    }
    return render(request, 'main/photo_home.html', context)

@login_required
def set_notification_zero(request):
    request.user.profile.notification_count = 0
    request.user.profile.save()
    response = {'success' : True}
    return JsonResponse(response)


@login_required
def post(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, 'main/photo_single_post.html', {'post' : post})


def report(request, id):
    post = get_object_or_404(Post, id=id)
    form = ReportForm(request.POST or None)
    if form.is_valid():
        form.instance.post = post
        form.instance.user = request.user
        form.save()

        messages.success(request, 'Your report has been submitted.')

        return redirect('main:index')

    return render(request, 'main/report.html', {'post' : post, 'form' : form})


@login_required
def category(request, category):
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list all users not followed by logged in user.
    suggested = User.objects.exclude(id__in=excluded).exclude(username=request.user.username)
    posts = Post.objects.filter(category=category).order_by('-created')

    context = {
        'suggested' : suggested,
        'posts' : posts
    }
    return render(request, 'main/category.html', context)


@login_required
def add_comment(request):
    data = json.loads(request.body)
    post_id = data['post_id']
    
    comment_text = data['comment_text']

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
            user_from=request.user,
            post=post,
            text=f"{request.user.get_full_name()} commented on {post.user.get_full_name()}'s post",
            notification_type='comment'
        )
        new_notification.save()

    response = {'success' : True}

    return JsonResponse(response)

@login_required
def like_toggle(request):
    data = json.loads(request.body)
    post_id = data['post_id']

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


         # create new notification if not logged in user
        if post.user != request.user:
            new_notification = Notification.objects.create(
                user=post.user,
                user_from=request.user,
                post=post,
                notification_type='heart',
                text=f'{request.user.get_full_name()} liked your post'
            )
            new_notification.save()
            # Increment notification count
            request.user.profile.notification_count += 1
            request.user.profile.save()
    
    response = {'success' : True}

    return JsonResponse(response)


@login_required
def upload(request):
    if request.method == 'POST':
        caption = request.POST['caption']
        image = request.FILES['file-input']
        category = request.POST['category']

        event = None
        event_url = None
        try:
            event = request.POST['event-check']
            event_url = request.POST['event-url']
            venue = request.POST['venue']
        except:
            pass
        
        if event:
            new_post = Post.objects.create(
                caption=caption,
                image=image,
                user=request.user,
                event=True,
                event_url=event_url,
                venue=venue,
                category=category
            )
            new_post.save()
        else:
            new_post = Post.objects.create(
                caption=caption,
                image=image,
                user=request.user,
                category=category
            )
            new_post.save()
        messages.success(request, 'Post successfully uploaded.')
        return redirect('main:index')
    return render(request, 'main/photo_upload.html')


@login_required
def explore(request):
    posts = Post.objects.annotate(count=Count('likes')).order_by('-count')
    # isolate all user ids of users followed by currently logged in user
    excluded = [user.following_user_id.id for user in request.user.following.all()]

    # list top 5 users with highest followers and exclude those already followed by logged in user.
    suggested = User.objects.exclude(id__in=excluded)\
                .exclude(username=request.user.username)\
                .annotate(count=Count('followers'))\
                .order_by('-count')[:5]

    context = {
        'posts' : posts,
        'suggested' : suggested
    }

    return render(request, 'main/photo_explore.html', context)

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    context = {
        'notifications':notifications
    }
    return render(request, 'main/photo_notifications.html', context)


@login_required
def search(request):
    posts = Post.objects.all()
    users = User.objects.all()
    query = request.GET['query']
    if query:
        posts = posts.filter(caption__icontains=query)
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query)
        ).distinct()

    context = {
        'posts' : posts,
        'users' : users,
        'query' : query
    }
    return render(request, 'main/search.html', context)


@login_required
def suggestion(request):
    form = SuggestionForm(request.POST or None)
    if form.is_valid():
        # Save the currently logged in user
        form.instance.user = request.user
        form.save()

        messages.success(request, 'Your suggestion has been submitted.')
        return redirect('main:index')
    
    context = {
        'form' : form
    }
    return render(request, 'main/suggestion.html', context)

