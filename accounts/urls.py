from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:target_id>', views.follow, name='follow'),
    path('unfollow/<int:target_id>', views.unfollow, name='unfollow')
]