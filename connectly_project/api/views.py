# File: api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

#for expired token session
#from django.utils import timezone
#from datetime import timedelta
#from rest_framework.authtoken.models import Token
#from django.contrib.auth import logout

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_resource(request):
    """
    A simple protected resource that requires authentication.
    Will return 401 Unauthorized if invalid or missing token.
    """
    return Response({
        "message": "You have access to this protected resource",
        "user": request.user.username,
        "email": request.user.email
    })