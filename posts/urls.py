from django.urls import path
from . import views
from .views import FeedView, PostDetailView, ProtectedView, UserListCreate, PostListCreate, CommentListCreate, add_comment, get_comments, like_post


urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('posts/', views.get_posts, name='get_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/reset-id/', views.reset_user_id, name='reset_user_id'),
    path('users/list-create/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/list-create/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('initialize-admin/', views.initialize_admin, name='initialize_admin'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'), 
    path('posts/<int:post_id>/comment/', add_comment, name='add-comment'),  
    path('posts/<int:post_id>/comments/', get_comments, name='get-comments'),
    path('feed/', FeedView.as_view(), name='feed'),
]