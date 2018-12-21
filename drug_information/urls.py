from django.urls import path

from .modules.api import drugs_api

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
]