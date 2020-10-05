from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:target_id>', views.follow, name='follow'),
    path('unfollow/<int:follow_id>', views.unfollow, name='unfollow'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile')
]