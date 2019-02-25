from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from doctor_profiles.models import DoctorQuestionnaire, QuestionnaireSection, Question, SectionQuestion, \
    Choice, ChoiceGroup, ChoiceGroupItem, QuestionChoiceGroup, Questionnaire


class QuestionnaireSerializer(TaggitSerializer, serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            'id',
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


class QuestionnairePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            'id',
            'slug',
            'name',
            'description',
            'instructions',
            'restriction',
        )


class DoctorQuestionnaireSerializer(serializers.ModelSerializer):
    questionnaire_object = serializers.SerializerMethodField('repr_questionnaire')

    def repr_questionnaire(self, obj):
        return QuestionnaireSerializer(obj.questionnaire).data

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
            'doctor',
            'questionnaire',
            'medical_institution',
            'questionnaire_object'
        )


class DoctorQuestionnaireCreateSerializer(serializers.ModelSerializer):
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
            'doctor',
            'questionnaire',
            'medical_institution'
        )


class DoctorQuestionnaireDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorQuestionnaire
        fields = ('id',)


class DoctorQuestionnairePublicSerializer(serializers.ModelSerializer):
    questionnaire_object = serializers.SerializerMethodField('repr_questionnaire')

    def repr_questionnaire(self, obj):
        return QuestionnairePublicSerializer(obj.questionnaire).data

    class Meta:
        model = DoctorQuestionnaire
        fields = (
            'id',
            'doctor',
            'questionnaire',
            'medical_institution',
            'questionnaire_object'
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
            'questionnaire'
        )


class QuestionnaireSectionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireSection
        fields = (
            'id',
            'order',
            'name',
            'description',
            'instructions',
            'questionnaire'
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'slug',
            'created',
            'last_updated',
            'metadata',
            'name',
            'text',
            'img',
            'answer_type',
            'answer_selection_type',
            'answer_data_type',
            'restriction',
            'created_by'
        )


class QuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'slug',
            'name',
            'text',
            'img',
        )


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'metadata',
            'name',
            'text',
            'img',
            'answer_type',
            'answer_selection_type',
            'answer_data_type',
            'restriction',
            'created_by'
        )


class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'metadata',
            'name',
            'text',
            'img',
            'answer_type',
            'answer_selection_type',
            'answer_data_type',
            'restriction',
            'created_by'
        )


class SectionQuestionSerializer(serializers.ModelSerializer):
    question_object = serializers.SerializerMethodField('repr_question')
    section_object = serializers.SerializerMethodField('repr_section')

    def repr_question(self, obj):
        return QuestionSerializer(obj.question).data

    def repr_section(self, obj):
        return QuestionnaireSectionSerializer(obj.section).data

    class Meta:
        model = SectionQuestion
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'order',
            'fork_map',
            'question_flow',
            'question',
            'section',
            'question_object',
            'section_object',
        )


class SectionQuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionQuestion
        fields = (
            'id',
            'order',
            'section',
            'question'
        )


class SectionQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionQuestion
        fields = (
            'order',
            'fork_map',
            'question_flow',
            'question',
            'section'
        )


class SectionQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionQuestion
        fields = (
            'id',
            'order',
            'fork_map',
            'question_flow',
            'question',
            'section'
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
