from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from search_indexes.documents.analyzers.common_analyzers import html_strip


INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)
