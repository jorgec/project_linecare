from rest_framework import serializers
from doctor_profiles.constants import APPOINTMENT_TYPES
from doctor_profiles.models import PatientAppointment


class PatientByCheckupAggregateSerializer(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField('repr_type')
    type = serializers.CharField()
    type_count = serializers.IntegerField()

    def repr_type(self, obj):
        for at in APPOINTMENT_TYPES:
            if at[0] == obj['type']:
                return at[1]
        return obj['type']

    class Meta:
        model = PatientAppointment
        fields = (
            'type',
            'type_count',
            'type_display'
        )


