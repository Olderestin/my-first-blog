from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class ProfileIsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username