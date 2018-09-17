from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'user_type',
            'created',
            'parent',
        )


class AccountSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'username',
            'user_type'
        )


class AccountRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64, allow_blank=True)
    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)