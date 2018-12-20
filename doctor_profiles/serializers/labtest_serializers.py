from rest_framework import serializers

from doctor_profiles.models import LabTest


class LabTestSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField('repr_description')
    purpose = serializers.SerializerMethodField('repr_purpose')
    indication = serializers.SerializerMethodField('repr_indication')
    sample = serializers.SerializerMethodField('repr_sample')
    preparation = serializers.SerializerMethodField('repr_preparation')
    usage = serializers.SerializerMethodField('repr_usage')
    interpretation = serializers.SerializerMethodField('repr_interpretation')
    notes = serializers.SerializerMethodField('repr_notes')
    aliases = serializers.SerializerMethodField('repr_aliases')

    def repr_aliases(self, obj):
        return ', '.join(obj.aliases)

    def repr_description(self, obj):
        words = ' '.join(obj.description.split(' ')[:30])
        return f'{words}...'

    def repr_purpose(self, obj):
        words = ' '.join(obj.purpose.split(' ')[:20])
        return f'{words}...'

    def repr_indication(self, obj):
        words = ' '.join(obj.indication.split(' ')[:30])
        return f'{words}...'

    def repr_sample(self, obj):
        words = ' '.join(obj.sample.split(' ')[:10])
        return f'{words}...'

    def repr_preparation(self, obj):
        words = ' '.join(obj.preparation.split(' ')[:10])
        return f'{words}...'

    def repr_usage(self, obj):
        words = ' '.join(obj.usage.split(' ')[:20])
        return f'{words}...'

    def repr_notes(self, obj):
        words = ' '.join(obj.notes.split(' ')[:20])
        return f'{words}...'

    def repr_interpretation(self, obj):
        words = ' '.join(obj.interpretation.split(' ')[:20])
        return f'{words}...'

    class Meta:
        model = LabTest
        fields = (
            'id',
            'slug',
            'name',
            'aliases',
            'description',
            'purpose',
            'indication',
            'sample',
            'preparation',
            'usage',
            'interpretation',
            'notes',
        )
