from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username_validator = UnicodeUsernameValidator()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
        )

        return user

    class Meta:
        model = User
        fields = ("username", "password", "full_name")
