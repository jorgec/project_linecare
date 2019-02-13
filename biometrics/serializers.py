from rest_framework import serializers

from biometrics.models import Biometric


class BiometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometric
        fields = (
            'height',
            'weight',
            'blood_type',
        )
