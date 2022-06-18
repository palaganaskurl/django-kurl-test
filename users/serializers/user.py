from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UnauthenticatedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']
