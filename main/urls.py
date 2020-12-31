from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>', views.post, name='post'),
    path('report/<int:id>', views.report, name='report'),
    path('category/<str:category>/', views.category, name='category'),
    path('comment/', views.add_comment, name='add_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('like/', views.like_toggle, name='like'),
    path('upload/', views.upload, name='upload'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('explore/', views.explore, name='explore'),
    path('notifications/', views.notifications, name='notifications'),
    path('search/', views.search, name='search'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('inquiry/<int:post_id>/', views.inquiry, name='inquiry'),
    path('set_notification_zero/', views.set_notification_zero, name='set_notification_zero'),
]

