from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user
            and request.user.rol == "admin"
        )


class IsTeacherUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user
            and request.user.rol == "teacher"
        )


class IsAdminOrTeacherUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user
            and request.user.rol == "admin"
            or request.user.rol == "teacher"
        )


class IsStudentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user
            and request.user.rol == "user"
        )
