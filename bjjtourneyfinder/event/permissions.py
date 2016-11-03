from rest_framework import permissions


class EventPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        owner = request.user.is_authenticated and obj.author == request.user
        return owner or request.user.is_admin


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin
