from rest_framework.permissions import BasePermission


class OnlyAdminCanCreateDeleteMovie(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return bool(request.user and request.user.is_staff
                        and request.user.is_superuser)

        return True


class OnlyCriticCanCreateUpdateReview(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return bool(request.user and request.user.is_staff
                        and not request.user.is_superuser)

        return True


class OnlyUserCanCreateUpdateComment(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return bool(request.user and not request.user.is_staff
                        and not request.user.is_superuser)

        return True
