from rest_framework import serializers

from accounts.models import Account
from profiles.serializers import PrivateProfileSerializer, PublicProfileSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'created',
            'parent',
        )


class AccountSerializerPublic(serializers.ModelSerializer):
    base_profile = PublicProfileSerializer(read_only=True)

    class Meta:
        model = Account
        fields = (
            'username',
            'first_name',
            'last_name',
            'user_type',
            'base_profile'
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


class AccountWithProfileSerializerPrivate(serializers.ModelSerializer):
    base_profile = PrivateProfileSerializer(read_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'created',
            'parent',
            'base_profile'
        )
