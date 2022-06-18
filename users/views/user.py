from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUserDataOrReadOnly
from users.serializers.user import UnauthenticatedUserSerializer
from users.serializers.user import UserSerializer
from users.views.password import PasswordSerializer


class UserViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()

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
        elif self.action == 'partial_update':
            permission_classes = [
                IsAuthenticated,
                TokenHasReadWriteScope,
                IsUserDataOrReadOnly,
            ]

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

    # noinspection PyUnusedLocal
    def partial_update(self, request, pk=None):
        user = self.get_object()
        password_serializer = PasswordSerializer(data=request.data)
        is_valid = password_serializer.is_valid()

        if not user.check_password(
            password_serializer.data.get('old_password')
        ):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_valid:
            return Response(
                password_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password_serializer.data.get('new_password'))
        user.save()

        user_serializer = UserSerializer(user)

        return Response(user_serializer.data)
