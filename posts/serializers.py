from rest_framework import serializers
from posts.models import Like, Comment, Post, User  # For creating serializers

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
        extra_kwargs = {'post': {'required': False}}  # Make post optional

    def create(self, validated_data):
        """
        Overriding create to ensure 'post' exists before saving.
        """
        post_id = self.context.get('post_id')  # Get post_id from the view
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({"post": "Post not found."}) 

        validated_data['post'] = post  # Assign post manually
        return super().create(validated_data)


