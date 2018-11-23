from rest_framework import serializers

from . import models


class ProvinceCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProvinceCoordinate
        fields = ('id',
                  'lat',
                  'lon',
                  )


class CityCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CityCoordinate
        fields = ('id',
                  'lat',
                  'lon',
                  )


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ('id',
                  'slug',
                  'name',
                  )


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = ('id',
                  'slug',
                  'name',
                  )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ('id',
                  'slug',
                  'name',
                  )


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class LocationNestedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = (
            'id',
            'name',
            'slug',
        )


class LocationNestedProvinceSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = models.Province
        fields = (
            'id',
            'name',
            'slug',
            'cities'
        )

    def get_cities(self, obj):
        queryset = models.City.objects.filter(province=obj)
        return LocationNestedCitySerializer(queryset, many=True, read_only=True).data


class LocationNestedRegionSerializer(serializers.ModelSerializer):
    provinces = serializers.SerializerMethodField()

    class Meta:
        model = models.Region
        fields = (
            'id',
            'name',
            'slug',
            'provinces'
        )

    def get_provinces(self, obj):
        queryset = models.Province.objects.filter(region=obj)
        return LocationNestedProvinceSerializer(queryset, many=True, read_only=True).data
