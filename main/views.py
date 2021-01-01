from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile, UserFollowing
from django.db.models import Q, Count
from .models import Post, Like, Comment, Notification, Inquiry
from .forms import SuggestionForm, ReportForm
from django.contrib.auth.decorators import login_required
import json
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadhandler import InMemoryUploadedFile
from io import BytesIO
import sys
from django.core.mail import send_mail
from django.conf import settings

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
        
        # increment notification count of users.
        user.profile.notification_count += 1
        user.profile.save()

    response = {'success' : True, 'new_comment_id' : new_comment.id}

    return JsonResponse(response)


@login_required
def delete_comment(request):
    data = json.loads(request.body)
    comment_id = data['comment_id']

    comment = Comment.objects.get(id=comment_id)
    comment.delete()

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
            post.user.profile.notification_count += 1
            post.user.profile.save()
    
    response = {'success' : True}

    return JsonResponse(response)


def watermark_image(image):
    image_to_watermark = Image.open(image)
    width, height = image_to_watermark.size
    draw = ImageDraw.Draw(image_to_watermark)
    text = "Earthruh"

    font = ImageFont.load_default()
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font)
    output = BytesIO()
    image_to_watermark.save(output, format='PNG')
    output.seek(0)
    watermarked_image = InMemoryUploadedFile(
        output, 'ImageField', image.name, 'image/png', sys.getsizeof(output), None)
    image_to_watermark.show()

    return watermarked_image

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
            
        # Add watermark to image
        image = watermark_image(image)
        
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

def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        caption = request.POST['caption']
        category = request.POST['category']

        event = None
        event_url = None
        image = None

        try:
            event = request.POST['event-check']
            event_url = request.POST['event-url']
            venue = request.POST['venue']
        except:
            pass
        try:
            # Add watermark to image
            image = watermark_image(request.FILES['file-input'])
        except:
            image = post.image

        if event:
            post.caption = caption
            post.image = image
            post.category = category
            post.event = True
            post.event_url = event_url
            post.venue = venue
        else:
            post.event = False
            post.event_url = ''
            post.venue = ''
            post.caption = caption
            post.image = image
            post.category = category
        
        post.save()
        messages.success(request, 'Post successfully edited.')
        return redirect('accounts:profile')
    return render(request, 'main/edit_post.html', {'post' : post})


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

@login_required
def inquiry(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        reason = request.POST['reason']
        email = request.POST['email']
        phone_number = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        country = request.POST['country']
        message = request.POST['message']
        
        new_inquiry = Inquiry.objects.create(
            post=post,
            post_author=post.user.username,
            username_of_inquirer=request.user.username,
            first_name=first_name,
            last_name=last_name,
            reason=reason,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            message=message
        )
        new_inquiry.save()

        # Send Mail
        send_mail(
            'Your Inquiry',
            'Your inquiry has been received.',
            settings.EMAIL_HOST_USER,
            [email, 'earthruh@gmail.com'],
            fail_silently=False
        )
        messages.success(request, 'Your inquiry has been submitted')
        return redirect('main:index')
    return render(request, 'main/inquiry.html')