from rest_framework.permissions import BasePermission

class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admin users to edit any post
        if request.user.is_staff:
            return True
        # Allow only post authors to edit their posts
        return obj.author == request.user