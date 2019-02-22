from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from doctor_profiles.models import DoctorQuestionnaire, QuestionnaireSection, Question, SectionQuestion, \
    Choice, ChoiceGroup, ChoiceGroupItem, QuestionChoiceGroup, Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            'slug',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'name',
            'description',
            'instructions',
            'restriction',
        )


class DoctorQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorQuestionnaire
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'is_creator',
            'is_required',
            'hook_location',
        )


class QuestionnaireSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireSection
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'order',
            'name',
            'description',
            'instructions',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'slug',
            'created',
            'last_updated',
            'metadata',
            'fork_map',
            'is_approved',
            'name',
            'text',
            'img',
            'answer_type',
            'answer_selection_type',
            'answer_data_type',
            'question_flow',
        )


class SectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionQuestion
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'order',
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'name',
            'text',
            'img',
            'value',
        )


class ChoiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroup
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'name',
        )


class ChoiceGroupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroupItem
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'order',
        )


class QuestionChoiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoiceGroup
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
        )
