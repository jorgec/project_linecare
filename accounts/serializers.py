from rest_framework import serializers

from accounts.models import Account
from biometrics.models import Biometric
from biometrics.serializers import BiometricSerializer
from profiles.serializers import PrivateProfileSerializer, PublicBaseProfileSerializer, BaseProfilePrivateSerializerFull


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'user_type',
            'created',
            'parent',
        )


class AccountSerializerPublic(serializers.ModelSerializer):
    base_profile = PublicBaseProfileSerializer()
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'user_type',
            'base_profile'
        )


class AccountRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64, allow_blank=True, required=False)

    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'password',
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)


class AccountWithProfileSerializerPrivate(serializers.ModelSerializer):
    base_profile = BaseProfilePrivateSerializerFull(read_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'user_type',
            'created',
            'parent',
            'base_profile'
        )


class AccountWithProfileAndBiometricsPrivate(serializers.ModelSerializer):
    base_profile = BaseProfilePrivateSerializerFull(read_only=True)
    profile_biometrics = serializers.SerializerMethodField('repr_biometrics')

    def repr_biometrics(self, obj):
        bm = Biometric.objects.get(profile=obj.base_profile())
        return BiometricSerializer(bm).data

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'user_type',
            'created',
            'parent',
            'base_profile',
            'profile_biometrics'
        )
