import json
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post


# User Views
def get_users(request):
   # Retrive details
   try:
       users = list(User.objects.values('id', 'username', 'email', 'created_at'))
       return JsonResponse(users, safe=False)
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)
  
@csrf_exempt
def create_user(request):
   if request.method == 'POST':
       try:
           data = json.loads(request.body)
           user = User.objects.create(username=data['username'], email=data['email'])
           return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=400)
   else:
       return JsonResponse({'error': 'GET method not allowed on this endpoint.'}, status=405)


# Post Views
def get_posts(request):
  # Retrieve all posts with their details.
   try:
       posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
       return JsonResponse(posts, safe=False)
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_post(request):
   # Create a new post.
   if request.method == 'POST':
       try:
           data = json.loads(request.body)
           author = User.objects.get(id=data['author'])
           post = Post.objects.create(content=data['content'], author=author)
           return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
       except User.DoesNotExist:
           return JsonResponse({'error': 'Author not found'}, status=404)
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=400)
      
@csrf_exempt
def delete_user(request, user_id):
   if request.method == 'DELETE':
       try:
           user = User.objects.get(id=user_id)  # Get the user by ID
           user.delete()  # Delete the user from the database
           return JsonResponse({'message': 'User deleted successfully'}, status=204)
       except User.DoesNotExist:
           return JsonResponse({'error': 'User not found'}, status=404)
   else:
       return JsonResponse({'error': 'Method not allowed'}, status=405)
  
@csrf_exempt
def reset_user_id(request):
   try:
       with connection.cursor() as cursor:
           # For SQLite
           cursor.execute("DELETE FROM sqlite_sequence WHERE name='yourapp_user';")


           # For PostgreSQL
           # cursor.execute("SELECT setval(pg_get_serial_sequence('yourapp_user', 'id'), 1, false);")


           # For MySQL
           # cursor.execute("ALTER TABLE yourapp_user AUTO_INCREMENT = 1;")


       return JsonResponse({'message': 'User ID sequence reset successfully'}, status=200)
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=400)