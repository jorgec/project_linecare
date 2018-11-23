from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r'region', api.RegionViewSet)
router.register(r'province', api.ProvinceViewSet)
router.register(r'city', api.CityViewSet)
# router.register(r'provincecoordinate', api.ProvinceCoordinateViewSet)
# router.register(r'citymedia', api.CityMediaViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    # url(r'^api/v1/', include(router.urls), name="api_location_refs"),

    # regions
    # path('api/v1/regions', api.LocationNestedRegionView.as_view(), name='api_locations_regions_of_country'),

    # cities

    path('api/v1/cities_of_province', api.CitiesOfProvinceViewSet.as_view(), name="api_location_cities_of_province"),
    path('api/v1/city/coordinates', api.CityCoordinateView.as_view(), name='api_location_city_coordinates'),

    # provinces
    url(r'^api/v1/provinces_of_region/$', api.ProvincesofRegionViewSet.as_view(), name="api_location_provinces_of_region"),

    # regions
    url(r'^api/v1/regions/$', api.RegionViewSet.as_view({'get': 'list'}), name='api_location_region_list')

)
