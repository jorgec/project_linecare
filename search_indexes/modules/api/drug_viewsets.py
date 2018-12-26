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

from elasticsearch_dsl import DateHistogramFacet, RangeFacet

from ...documents import DrugDocument
from ...serializers import DrugDocumentSerializer

__all__ = (
    'BaseDrugDocumentViewSet',
)


class BaseDrugDocumentViewSet(BaseDocumentViewSet):
    """Base DrugDocument ViewSet."""

    document = DrugDocument
    # serializer_class = DrugDocumentSerializer
    serializer_class = DrugDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        # PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        # FacetedSearchFilterBackend,
        # SuggesterFilterBackend,
        # FunctionalSuggesterFilterBackend,
        HighlightBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
        'generic_names',
        'active_ingredients',
    )
    # Define highlight fields
    highlight_fields = {
        'name': {
            'enabled': True,
            'options': {
                'pre_tags': ["<b>"],
                'post_tags': ["</b>"],
            }
        },
    }
    # Define filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
                LOOKUP_FILTER_TERMS,
            ],
        },
        'name': 'name',
        'base_name': 'base_name',
        'generic_names': 'generic_names.raw',
        'active_ingredients': 'active_ingredients.raw',
        # This has been added to test `exists` filter.
        'non_existent_field': 'non_existent_field',
        # This has been added to test `isnull` filter.
        'null_field': 'null_field',
    }
    # Define ordering fields
    ordering_fields = {
        'name': 'name.raw',
        'id': 'id',
    }
    # Specify default ordering
    ordering = ('name', 'id',)
