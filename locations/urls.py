from django.conf.urls import url, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r'region', api.RegionViewSet)
router.register(r'province', api.ProvinceViewSet)
router.register(r'city', api.CityViewSet)
router.register(r'provincecoordinate', api.ProvinceCoordinateViewSet)
router.register(r'citycoordinate', api.CityCoordinateViewSet)
# router.register(r'citymedia', api.CityMediaViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    # url(r'^api/v1/', include(router.urls), name="api_location_refs"),

    # cities
    url(r'^api/v1/cities_of_province/$', api.CitiesOfProvinceViewSet.as_view(), name="api_cities_of_province"),

    # provinces
    url(r'^api/v1/provinces_of_region/$', api.ProvincesofRegionViewSet.as_view(), name="api_provinces_of_region"),

)
