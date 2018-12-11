from rest_framework import serializers

from datesdim.constants import MONTH_CHOICES
from datesdim.models import DateDim, TimeDim


class DateDimSerializer(serializers.ModelSerializer):
    month_name = serializers.SerializerMethodField('repr_month_name')

    def repr_month_name(self, obj):
        return MONTH_CHOICES[obj.month - 1][1]

    class Meta:
        model = DateDim
        fields = (
            'id',
            'year',
            'month',
            'day',
            'date_obj',
            'day_name',
            'week_day',
            'week_month',
            'week_year',
            'month_name'
        )


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
            'format_12',
        )
