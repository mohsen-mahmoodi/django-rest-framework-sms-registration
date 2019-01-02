from rest_framework.permissions import IsAuthenticated


class IsRegistered(IsAuthenticated):
    message = 'The user is not registered.'

    def has_permission(self, request, view):
        return super(IsRegistered, self).has_permission(request, view) and request.user.is_registered

