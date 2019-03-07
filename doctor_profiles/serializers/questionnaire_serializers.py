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
    questionnaire = serializers.SerializerMethodField('repr_questionnaire')

    def repr_question(self, obj):
        return QuestionSerializer(obj.question).data

    def repr_questionnaire(self, obj):
        return obj.section.questionnaire.id

    class Meta:
        model = SectionQuestion
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'order',
            'fork_map',
            'question_flow',
            'question',
            'section',
            'question_object',
            'questionnaire'
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


class QuestionnaireSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('repr_questions')

    def repr_questions(self, obj):
        questions = obj.get_questions_rel()
        if questions.count() > 0:
            return SectionQuestionSerializer(questions, many=True).data
        return None

    class Meta:
        model = QuestionnaireSection
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'order',
            'name',
            'description',
            'instructions',
            'questionnaire',
            'questions'
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
            'name',
            'text',
            'img',
            'value',
        )


class ChoicePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'id',
            'name',
            'text',
            'img',
            'value',
        )


class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'metadata',
            'name',
            'text',
            'img',
            'value',
        )


class ChoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'id',
            'metadata',
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
            'metadata',
            'name',
        )


class ChoiceGroupPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroup
        fields = (
            'id',
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
            'order',
        )


class ChoiceGroupItemPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroupItem
        fields = (
            'id',
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
            'question'
        )


class QuestionChoiceGroupPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoiceGroup
        fields = (
            'id',
            'question'
        )
