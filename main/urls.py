from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.category, name='category'),
    path('comment/', views.add_comment, name='add_comment'),
    path('like/', views.like_toggle, name='like'),
    path('upload/', views.upload, name='upload'),
    path('explore/', views.explore, name='explore'),
    path('notifications/', views.notifications, name='notifications'),
    path('search/', views.search, name='search'),
    path('suggestion/', views.suggestion, name='suggestion')
]

