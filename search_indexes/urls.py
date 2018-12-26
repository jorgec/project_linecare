from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from search_indexes.modules.api.doctor_viewsets import BaseDoctorDocumentViewSet
from search_indexes.modules.api.drug_viewsets import BaseDrugDocumentViewSet
from search_indexes.modules.api import drug_api
from search_indexes.modules.api import doctor_api

router = DefaultRouter()

drugs = router.register(r'drugs',
                        BaseDrugDocumentViewSet,
                        base_name='drugdocument')
doctors = router.register(r'doctors',
                          BaseDoctorDocumentViewSet,
                          base_name='doctordocument')


urlpatterns = [
    path('', include(router.urls)),

]

version = 'api/v1'

urlpatterns += [
    path(f'{version}/drugs',
         drug_api.ApiElasticSearchDrugLookup.as_view(),
         name='api_es_drugs_search'),
    path(f'{version}/doctors',
         doctor_api.ApiElasticSearchDoctorLookup.as_view(),
         name='api_es_doctors_search'),
]