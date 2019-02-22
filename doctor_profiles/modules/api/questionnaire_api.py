from doctor_profiles import models
from doctor_profiles import serializers
from rest_framework import viewsets, permissions


class QuestionnaireViewSet(viewsets.ModelViewSet):
    """ViewSet for the Questionnaire class"""

    queryset = models.Questionnaire.objects.all()
    serializer_class = serializers.QuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorQuestionnaireViewSet(viewsets.ModelViewSet):
    """ViewSet for the DoctorQuestionnaire class"""

    queryset = models.DoctorQuestionnaire.objects.all()
    serializer_class = serializers.DoctorQuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionnaireSectionViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionnaireSection class"""

    queryset = models.QuestionnaireSection.objects.all()
    serializer_class = serializers.QuestionnaireSectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Question class"""

    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionQuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the SectionQuestion class"""

    queryset = models.SectionQuestion.objects.all()
    serializer_class = serializers.SectionQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Choice class"""

    queryset = models.Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChoiceGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChoiceGroup class"""

    queryset = models.ChoiceGroup.objects.all()
    serializer_class = serializers.ChoiceGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChoiceGroupItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChoiceGroupItem class"""

    queryset = models.ChoiceGroupItem.objects.all()
    serializer_class = serializers.ChoiceGroupItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionChoiceGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionChoiceGroup class"""

    queryset = models.QuestionChoiceGroup.objects.all()
    serializer_class = serializers.QuestionChoiceGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
