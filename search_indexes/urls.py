from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from search_indexes.modules.api.drug_viewsets import BaseDrugDocumentViewSet
from search_indexes.modules.api import drug_api

router = DefaultRouter()

drugs = router.register(r'drugs',
                        BaseDrugDocumentViewSet,
                        base_name='drugdocument')


urlpatterns = [
    path('', include(router.urls)),

]

version = 'api/v1'

urlpatterns += [
    path(f'{version}/drugs',
         drug_api.ApiElasticSearchDrugLookup.as_view(),
         name='api_es_drugs_search'),
]