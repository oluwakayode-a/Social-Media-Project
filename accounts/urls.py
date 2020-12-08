from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:target_id>', views.follow, name='follow'),
    path('unfollow/<int:target_id>', views.unfollow, name='unfollow'),
    path('profile/', views.profile, name='profile'),
    path('<str:user>/profile/', views.user, name='user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_interests/', views.edit_interests, name='edit_interests'),
    path('followers/', views.followers, name='followers'),
    path('following/', views.following, name='following')
]