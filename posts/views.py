from django.db import connection  # For resetting ID sequences or direct database operations
from rest_framework.decorators import api_view  # For defining DRF API views
from rest_framework.views import APIView  # For defining DRF API views
from rest_framework.generics import RetrieveAPIView  # For defining DRF API views
from rest_framework import status  # For HTTP status codes
from rest_framework.response import Response
from posts.serializers import CommentSerializer, PostSerializer, UserSerializer  # DRF's Response object for API responses
from .models import User, Post, Comment  # Importing models for queries and serializers


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


