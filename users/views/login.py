from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib import common
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers.login import LoginSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def post(self, request, **kwargs):
        login_serializer = LoginSerializer(data=request.data)

        if not login_serializer.is_valid():
            return Response(
                login_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=login_serializer.data.get('email'), is_active=True)
        except ObjectDoesNotExist:
            return Response('Account not activated or invalid credentials!', status=status.HTTP_401_UNAUTHORIZED)

        valid_password = user.check_password(login_serializer.data.get('password'))

        if not valid_password:
            return Response('Invalid credentials!', status=status.HTTP_401_UNAUTHORIZED)

        application = Application.objects.get(client_id=settings.CLIENT_ID)

        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = AccessToken(
            user=user,
            scope='read write groups',
            expires=expires,
            token=common.generate_token(),
            application=application
        )
        access_token.save()

        refresh_token = RefreshToken(
            user=user,
            token=common.generate_token(),
            application=application,
            access_token=access_token
        )
        refresh_token.save()

        return Response({
            'access_token': access_token.token,
            'refresh_token': refresh_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'scopes': access_token.scopes,
            'token_type': 'Bearer'
        })
