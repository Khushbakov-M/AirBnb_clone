from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        return user == request.user