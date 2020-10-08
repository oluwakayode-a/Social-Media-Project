from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('comment', views.add_comment, name='add_comment'),
    path('like/<int:post_id>', views.like_toggle, name='like'),
]

