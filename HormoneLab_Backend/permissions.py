from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return request.user.is_staff  



from rest_framework import permissions


class IsSuperAdminOrDoctorOwner(permissions.BasePermission):
    """
    SuperAdmin সব কিছু করতে পারবে,
    Doctor শুধু নিজের payment দেখতে/approve করতে পারবে,
    Staff (executive, hospital authority) কিছুই পারবে না।
    """
    def has_object_permission(self, request, view, obj):
        # SuperAdmin সব কিছু পারবে
        if request.user and request.user.is_superuser:
            return True

        # শুধু doctor তার নিজের payment এ GET/PUT/PATCH করতে পারবে
        if request.user and request.user.is_authenticated:
            if obj.doctor == request.user:
                if request.method in ['GET', 'PUT', 'PATCH']:
                    return True

        # অন্য কেউ (staff সহ) access পাবে না
        return False
