from django.db import connection  # For resetting ID sequences or direct database operations
from rest_framework.decorators import api_view  # For defining DRF API views
from rest_framework.views import APIView  # For defining DRF API views
from rest_framework.generics import RetrieveAPIView  # For defining DRF API views
from rest_framework import status  # For HTTP status codes
from rest_framework.response import Response
from posts.serializers import CommentSerializer, PostSerializer, UserSerializer  # DRF's Response object for API responses
from .models import User, Post, Comment  # Importing models for queries and serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from factories.post_factory import PostFactory


# User Views
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
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({'id': serializer.instance.id, 'message': 'User created successfully'}, status=201)
       return Response(serializer.errors, status=400)
   except Exception as e:
       return Response({'error': str(e)}, status=500)
user = User.objects.create_user(username="new_user", password="secure_pass123")
print(user.password)  # Outputs a hashed password
user = authenticate(username="new_user", password="secure_pass123")
if user is not None:
    print("Authentication successful!")
else:
    print("Invalid credentials.")
admin_group = Group.objects.create(name="Admin")
user = User.objects.get(username="admin_user")
user.groups.add(admin_group)


@api_view(['GET'])
def get_posts(request):
   try:
       posts = Post.objects.all()
       serializer = PostSerializer(posts, many=True)
       return Response(serializer.data)
   except Exception as e:
       return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def create_post(request):
   try:
       serializer = PostSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({'id': serializer.instance.id, 'message': 'Post created successfully'}, status=201)
       return Response(serializer.errors, status=400)
   except Exception as e:
       return Response({'error': str(e)}, status=500)
      
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
  
class PostDetailView(RetrieveAPIView):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


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

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"message": "Authenticated!"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Exclude sensitive fields like password

class CreatePostView(APIView):
    def post(self, request):
        data = request.data
        try:
            post = PostFactory.create_post(
                post_type=data['post_type'],
                title=data['title'],
                content=data.get('content', ''),
                metadata=data.get('metadata', {})
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
