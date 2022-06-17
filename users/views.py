
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers.register import RegisterSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
