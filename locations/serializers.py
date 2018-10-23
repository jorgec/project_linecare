from rest_framework import serializers

from . import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ('id',
                  'slug',
                  'name',
                  'created',
                  'last_updated',
                  'code',
                  )


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = ('id',
                  'slug',
                  'name',
                  'created',
                  'last_updated',
                  )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ('id',
                  'slug',
                  'name',
                  'created',
                  'last_updated',
                  )


class ProvinceCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProvinceCoordinate
        fields = ('id',
                  'pk',
                  'created',
                  'last_updated',
                  'lat',
                  'lon',
                  'is_approved',
                  )


class CityCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CityCoordinate
        fields = ('id',
                  'pk',
                  'created',
                  'last_updated',
                  'lat',
                  'lon',
                  'is_approved',
                  )
