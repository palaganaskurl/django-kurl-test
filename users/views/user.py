from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers.user import UserSerializer, UnauthenticatedUserSerializer


class UserViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def get_authenticators(self):
        authenticators = []

        if self.request.headers.get('Authorization'):
            authenticators = [OAuth2Authentication]

        return [authenticator() for authenticator in authenticators]

    def get_permissions(self):
        permission_classes = []

        if self.action == 'retrieve':
            if self.request.headers.get('Authorization'):
                permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

        return [permission() for permission in permission_classes]

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        if self.get_authenticate_header(self.request):
            serializer = UserSerializer(user)
        else:
            serializer = UnauthenticatedUserSerializer(user)

        return Response(serializer.data)
