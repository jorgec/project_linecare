from rest_framework import serializers

from datesdim.models import DateDim, TimeDim


class DateDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateDim
        fields = '__all__'


class TimeDimSerializer(serializers.ModelSerializer):
    format_24 = serializers.SerializerMethodField('repr_format_24')
    format_12 = serializers.SerializerMethodField('repr_format_12')

    def repr_format_24(self, obj):
        return obj.as_string()

    def repr_format_12(self, obj):
        return obj.format_12()

    class Meta:
        model = TimeDim
        fields = (
            'hour',
            'minute',
            'minutes_since',
            'format_24',
            'format_12'
        )
