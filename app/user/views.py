"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


# DRF provides template CBVs, which are organized according to the
# REST convention.
# The following class is used for the customization and overriding
# the default behavior
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    # View reacts for the incoming request, by calling serializer
    # class - validation first,
    # and if validation pass, then .create method is called
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # this is only for browsable api (Swagger) - without renderer,
    # it wont be present in browsable api
    # it can be considered as an issue of ObtainAuthToken view -
    # why it is not enabled by default in browsable api
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    # require the user is authenticated
    permission_classes = [permissions.IsAuthenticated, ]

    # override get_object. When GET request is sent, then
    # authenticated user is returned.
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
