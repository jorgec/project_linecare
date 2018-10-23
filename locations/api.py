from rest_framework import viewsets, permissions, generics

from . import models
from . import serializers


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Region class"""

    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ProvinceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Province class"""

    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for the City class"""

    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    # permission_classes = [permissions.IsAuthenticated]


class ProvincesofRegionViewSet(generics.ListAPIView):
    """Viewset for provinces of region"""
    serializer_class = serializers.ProvinceSerializer

    def get_queryset(self):
        region = self.request.GET.get('region')
        return models.Province.objects.filter(region=region).order_by('name')


class CitiesOfProvinceViewSet(generics.ListAPIView):
    """Viewset for cities of province"""
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        province = self.request.GET.get('province')
        return models.City.objects.filter(province=province).order_by('name')


class ProvinceCoordinateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProvinceCoordinate class"""

    queryset = models.ProvinceCoordinate.objects.all()
    serializer_class = serializers.ProvinceCoordinateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CityCoordinateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CityCoordinate class"""

    queryset = models.CityCoordinate.objects.all()
    serializer_class = serializers.CityCoordinateSerializer
    # permission_classes = [permissions.IsAuthenticated]



