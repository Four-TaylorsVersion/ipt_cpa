from django.db import connection  # For resetting ID sequences or direct database operations
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view  # For defining DRF API views
from rest_framework.views import APIView  # For defining DRF API views
from rest_framework.generics import RetrieveAPIView  # For defining DRF API views
from rest_framework import status  # For HTTP status codes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from factories.post_factory import PostFactory
from posts.serializers import CommentSerializer, PostSerializer, UserSerializer  # DRF's Response object for API responses
from posts.models import Like, Post, Comment, User  # Importing models for queries and serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from singletons.logger_singleton import LoggerSingleton
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination

logger = LoggerSingleton().get_logger()

@api_view(['GET'])
def initialize_admin(request):
    admin_group, created = Group.objects.get_or_create(name="Admin")
    
    try:
        user = User.objects.get(username="admin_user")
        user.groups.add(admin_group)
        user.save()  # Ensure changes are saved
        return Response({"message": "Admin group added to user."}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Admin user not found."}, status=404)

# User Views to be used in the API
@api_view(['GET'])
def get_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)  # Serialize multiple users
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def create_user(request):
    try:
        # Get username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with this username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists. Please choose another one."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user using the given credentials (with automatic password hashing)
        user = User.objects.create_user(username=username, password=password)

        # Output the hashed password (just for demonstration)
        print(user.password)  # This will print the hashed version of the password

        # Authenticate using the same credentials
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            print("Authentication successful!")
            # Return a success response with user data
            return Response({"message": "User created and authenticated successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        else:
            print("Invalid credentials.")
            return Response({"error": "Authentication failed after user creation."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle any unexpected errors
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_posts(request):
    try:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        author = request.user
        post = PostFactory.create_post(
            post_type=request.data['post_type'],
            title=request.data['title'],
            content=request.data.get('content', ''),
            metadata=request.data.get('metadata', {}),
            author=author 
        )

        return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def reset_user_id(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='yourapp_user';")
        return Response({'message': 'User ID sequence reset successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
class AddCommentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})
    
    def patch(self, request, pk):
        """Allow partial updates to a post"""
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)  # Check if the user is allowed

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated!"})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        
        # Check if the user has already liked this post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"error": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Post liked successfully!"}, status=status.HTTP_201_CREATED)

    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data, context={"post_id": post_id})
    if serializer.is_valid():
        serializer.save(author=request.user) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


class FeedPagination(PageNumberPagination):
    page_size = 3

class FeedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = FeedPagination

    def get_queryset(self):
        # Retrieve posts sorted by newest first
        return Post.objects.all().order_by('-created_at')