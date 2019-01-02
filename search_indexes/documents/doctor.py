from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields

from doctor_profiles.models import DoctorProfile
# Name of the Elasticsearch index
from search_indexes.documents.analyzers.common_analyzers import html_strip

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@INDEX.doc_type
class DoctorDocument(DocType):
    id = fields.IntegerField(attr='id')
    name = fields.StringField(
        attr='name_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    specializations = fields.StringField(
        attr='specializations_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    degrees = fields.StringField(
        attr='degrees_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    associations = fields.StringField(
        attr='associations_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    diplomates = fields.StringField(
        attr='diplomates_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    fellowships = fields.StringField(
        attr='fellowships_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    insurance_providers = fields.StringField(
        attr='insurance_providers_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )
    medical_institutions = fields.StringField(
        attr='medical_institutions_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )

    addresses = fields.StringField(
        attr='addresses_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword')
        }
    )

    class Meta(object):
        model = DoctorProfile
