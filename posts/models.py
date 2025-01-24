from django.db import models
from django.forms import ValidationError


class User(models.Model):
   username = models.CharField(max_length=100, unique=True) # User's unique username
   email = models.EmailField(unique=True) # User's unique email
   created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the user was created


   def __str__(self):
       return self.username


class Post(models.Model):
   title = models.CharField(max_length=100, default="Untitled")
   content = models.TextField() # The text content of the post
   author = models.ForeignKey(User, on_delete=models.CASCADE) # The user who created the post
   created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the post was created
   is_published = models.BooleanField(default=False) # Track published status


   def clean(self):
       if not self.title or self.title.strip() == "":
           raise ValidationError("Title cannot be empty.")


   def __str__(self):
       return self.content[:50]
  
class Comment(models.Model):
   text = models.TextField()
   author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
   post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"Comment by {self.author.username} on Post {self.post.id}"