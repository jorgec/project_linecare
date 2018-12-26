from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    BaseDocumentViewSet,
)

from search_indexes.documents import DoctorDocument
from search_indexes.serializers import DoctorDocumentSerializer


class BaseDoctorDocumentViewSet(BaseDocumentViewSet):
    document = DoctorDocument
    serializer_class = DoctorDocumentSerializer
    lookup_field = 'id'

    search_fields = (
        'name',
        'specializations',
        'degrees',
        'associations',
        'fellowships',
        'displomates',
        'insurance_providers',
        'medical_institutions',
        'addresses'
    )