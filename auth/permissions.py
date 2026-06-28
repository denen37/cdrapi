from rest_framework import permissions

class HasGroupPermission(permissions.BasePermission):
    group_name = None

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name=self.group_name).exists()
        )

class IsAdmin(HasGroupPermission):
    group_name = "admin"


class IsAnalyst(HasGroupPermission):
    group_name = "analyst"


class IsUser(HasGroupPermission):
    group_name = "user"