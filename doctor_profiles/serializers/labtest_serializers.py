from rest_framework import serializers

from doctor_profiles.models import LabTest, PatientLabTestRequest
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


class LabTestSerializer(serializers.ModelSerializer):
    description_excerpt = serializers.SerializerMethodField('repr_description')
    purpose_excerpt = serializers.SerializerMethodField('repr_purpose')
    indication_excerpt = serializers.SerializerMethodField('repr_indication')
    sample_excerpt = serializers.SerializerMethodField('repr_sample')
    preparation_excerpt = serializers.SerializerMethodField('repr_preparation')
    usage_excerpt = serializers.SerializerMethodField('repr_usage')
    interpretation_excerpt = serializers.SerializerMethodField('repr_interpretation')
    notes_excerpt = serializers.SerializerMethodField('repr_notes')
    aliases = serializers.SerializerMethodField('repr_aliases')

    def repr_aliases(self, obj):
        if obj.aliases:
            return ', '.join(obj.aliases)
        return None

    def repr_description(self, obj):
        if obj.description:
            words = ' '.join(obj.description.split(' ')[:30])
            return f'{words}...'
        return None

    def repr_purpose(self, obj):
        if obj.purpose:
            words = ' '.join(obj.purpose.split(' ')[:20])
            return f'{words}...'
        return None

    def repr_indication(self, obj):
        if obj.indication:
            words = ' '.join(obj.indication.split(' ')[:30])
            return f'{words}...'
        return None

    def repr_sample(self, obj):
        if obj.sample:
            words = ' '.join(obj.sample.split(' ')[:10])
            return f'{words}...'
        return None

    def repr_preparation(self, obj):
        if obj.preparation:
            words = ' '.join(obj.preparation.split(' ')[:10])
            return f'{words}...'
        return None

    def repr_usage(self, obj):
        if obj.usage:
            words = ' '.join(obj.usage.split(' ')[:20])
            return f'{words}...'
        return None

    def repr_notes(self, obj):
        if obj.notes:
            words = ' '.join(obj.notes.split(' ')[:20])
            return f'{words}...'
        return None

    def repr_interpretation(self, obj):
        if obj.interpretation:
            words = ' '.join(obj.interpretation.split(' ')[:20])
            return f'{words}...'
        return None

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
            'description_excerpt',
            'purpose_excerpt',
            'indication_excerpt',
            'sample_excerpt',
            'preparation_excerpt',
            'usage_excerpt',
            'interpretation_excerpt',
            'notes_excerpt',
        )


class PatientLabTestRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientLabTestRequest
        fields = (
            'checkup',
            'lab_test'
        )


class PatientLabTestRequestSerializer(serializers.ModelSerializer):
    lab_test = LabTestSerializer()
    requested_by = DoctorProfilePrivateSerializer()
    removed_by = DoctorProfilePrivateSerializer()
    class Meta:
        model = PatientLabTestRequest
        fields = '__all__'
