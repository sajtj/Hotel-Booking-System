from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ApiAuthMixin:
    """
    A mixin to enforce authentication for views.
    Extends DRF's authentication to allow JWT by default.
    """
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]