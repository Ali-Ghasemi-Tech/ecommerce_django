from rest_framework import permissions


class IsSuperUserOrSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj


class IsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj
