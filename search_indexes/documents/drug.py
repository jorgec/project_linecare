from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer

from drug_information.models import Drug

# Name of the Elasticsearch index
from search_indexes.documents.analyzers.common_analyzers import html_strip

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@INDEX.doc_type
class DrugDocument(DocType):
    id = fields.IntegerField(attr='id')

    name = fields.StringField(
        attr='name',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        },
    )

    base_name = fields.StringField(
        attr='base_name',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        },
    )

    generic_names = fields.StringField(
        attr='generic_name_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        },
    )

    active_ingredients = fields.KeywordField(
        attr='active_ingredients_indexing',
    )

    routes = fields.StringField(
        attr='routes_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
        },
    )

    pharm_class = fields.StringField(
        attr='pharm_class_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
        },
    )

    dosage_forms = fields.StringField(
        attr='dosage_forms_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
        },
    )

    class Meta(object):
        """Meta options."""

        model = Drug  # The model associate with this DocType
