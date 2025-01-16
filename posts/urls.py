from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('posts/', views.get_posts, name='get_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/reset-id/', views.reset_user_id, name='reset_user_id'),
]



