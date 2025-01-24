from rest_framework import serializers
from posts.models import Comment, Post, User  # For creating serializers


class UserSerializer(serializers.ModelSerializer):
   is_verified_email = serializers.BooleanField(source='is_verified', read_only=True) # Maps a model field
   user_name = serializers.CharField(source='username', read_only=True) # Maps a model field
  
   class Meta:
       model = User
       fields = ['id', 'username', 'email', 'created_at', 'is_verified_email', 'user_name']


       def validate_username(self, value):
           # Check if the username already exists
           if User.objects.filter(username=value).exists():
               raise serializers.ValidationError("The username is already taken.")
           return value
      
class PostSerializer(serializers.ModelSerializer):
   comments = serializers.StringRelatedField(many=True, read_only=True)  # Nested serializer for comments


   class Meta:
       model = Post
       fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']


class CommentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Comment
       fields = ['id', 'text', 'author', 'post', 'created_at']


   def validate_post(self, value):
       if not Post.objects.filter(id=value.id).exists():
           raise serializers.ValidationError("Post not found.")
       return value


   def validate_author(self, value):
       if not User.objects.filter(id=value.id).exists():
           raise serializers.ValidationError("Author not found.")
       return value
