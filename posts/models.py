from django.db import models
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128, default='')

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # <- Change related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # <- Change related_name
        blank=True
    )

    class Meta:
        db_table = 'posts_user' 
    
    def __str__(self):
        return self.username
class Post(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    
    POST_TYPES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    
    title = models.CharField(max_length=100, default="Untitled")
    content = models.TextField()
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
        default=TEXT,
    )
    metadata = models.JSONField(default=dict)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Use get_user_model()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def clean(self):
        if not self.title or self.title.strip() == "":
            raise ValidationError("Title cannot be empty.")

    def __str__(self):
        return self.content[:50]

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE)  # Use get_user_model()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Use get_user_model()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"