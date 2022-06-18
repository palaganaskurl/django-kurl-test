from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers.user import UserSerializer


class UserListViewSet(viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)
