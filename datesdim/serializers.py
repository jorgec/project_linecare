from rest_framework import serializers

from datesdim.models import DateDim, TimeDim


class DateDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateDim
        fields = '__all__'


class TimeDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeDim
        fields = '__all__'
