from django.contrib.auth import get_user_model
from posts.models import Post

class PostFactory:
    @staticmethod
    def create_post(post_type, title, content, metadata, author):
        # Validate author type
        if not isinstance(author, get_user_model()):
            raise ValueError("The 'author' must be a valid User instance.")
            
        # Validate post_type
        if post_type not in [choice[0] for choice in Post.POST_TYPES]:
            raise ValueError("Invalid post type")
            
        # Validate metadata for specific post types
        if post_type == 'image' and 'file_size' not in metadata:
            raise ValueError("Image posts require 'file_size' in metadata")
        if post_type == 'video' and 'duration' not in metadata:
            raise ValueError("Video posts require 'duration' in metadata")

        post = Post.objects.create(
            post_type=post_type,
            title=title,
            content=content,
            metadata=metadata,
            author=author
        )
        return post