from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.tokens import AccountActivationTokenGenerator


class ActivateUserAPIView(APIView):
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def get(self, request, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and AccountActivationTokenGenerator().check_token(
            user, kwargs.get('token')
        ):
            user.is_active = True
            user.save()

            return Response(
                'Thank you for your email confirmation. '
                'Now you can login your account.'
            )

        return Response('Activation link is invalid!')
