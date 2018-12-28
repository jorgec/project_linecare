from django.urls import path

from .modules.api import drugs_api
from .modules.api import drug_routes_api


#############################################################################
# API
#############################################################################
version = 'api/v1'

urlpatterns = [
    path(f'{version}/public/generics/list',
         drugs_api.ApiPublicGenericNameList.as_view(),
         name='api_public_generics_list'),
    path(f'{version}/public/drugs/list',
         drugs_api.ApiPublicDrugList.as_view(),
         name='api_public_drugs_list'),
    path(f'{version}/private/drugs/create',
         drugs_api.ApiPrivateDrugCreate.as_view(),
         name='api_private_drugs_create'),
    path(f'{version}/public/drug/detail',
         drugs_api.ApiPublicDrugDetail.as_view(),
         name='api_public_drug_detail'),

    path(f'{version}/public/drug_routes/list',
         drug_routes_api.ApiDrugRouteList.as_view(),
         name='api_public_drug_route_list'),
]