from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('follow/<int:target_id>', views.follow, name='follow'),
    path('unfollow/<int:target_id>', views.unfollow, name='unfollow'),
    path('profile/', views.profile, name='profile'),
    path('<str:user>/profile/', views.user, name='user'),
    path('<str:user>/profile/followers/', views.user_followers, name='user_followers'),
    path('<str:user>/profile/following/', views.user_following, name='user_following'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_interests/', views.edit_interests, name='edit_interests'),
    path('followers/', views.followers, name='followers'),
    path('following/', views.following, name='following'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('logout/', LogoutView.as_view(), name='logout'),
]