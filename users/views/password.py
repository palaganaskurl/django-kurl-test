from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
