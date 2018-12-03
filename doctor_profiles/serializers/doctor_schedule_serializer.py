from rest_framework import serializers


class DoctorScheduleCreateSerializer(serializers.Serializer):
    start = serializers.CharField()
    end = serializers.CharField()
    days = serializers.ListField()
