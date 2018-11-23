from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from locations.models import CityCoordinate, Country, Region
from locations.serializers import LocationNestedRegionSerializer
from . import models
from . import serializers


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Region class"""

    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [permissions.AllowAny]


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
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        region = self.request.GET.get('region')
        return models.Province.objects.filter(region=region).order_by('name')


class CitiesOfProvinceViewSet(generics.ListAPIView):
    """Viewset for cities of province"""
    serializer_class = serializers.CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        province = self.request.GET.get('province')
        return models.City.objects.filter(province=province).order_by('name')


# class ProvinceCoordinateViewSet(viewsets.ModelViewSet):
#     """ViewSet for the ProvinceCoordinate class"""
#
#     queryset = models.ProvinceCoordinate.objects.all()
#     serializer_class = serializers.ProvinceCoordinateSerializer
#     # permission_classes = [permissions.IsAuthenticated]


# class CityCoordinateViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CityCoordinate class"""
#
#     queryset = models.CityCoordinate.objects.all()
#     serializer_class = serializers.CityCoordinateSerializer
#     # permission_classes = [permissions.IsAuthenticated]

class CityCoordinateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            coords = get_object_or_404(CityCoordinate, id=id)
            serializer = serializers.CityCoordinateSerializer(coords)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class LocationNestedRegionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        country_id = request.GET.get('country', None)
        if not country_id:
            country = Country.objects.get(iso3='PHL')
        else:
            try:
                country = Country.objects.get(id=country_id)
            except Country.DoesNotExist:
                return Response(None, status=status.HTTP_404_NOT_FOUND)

        regions = Region.objects.filter(country=country)

        serializer = LocationNestedRegionSerializer(regions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
