from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()
# Create your views here.
def index(request):
    profiles = Profile.objects.exclude(user=request.user)

    context = {
        'profiles' : profiles
    }
    return render(request, 'main/index.html', context)