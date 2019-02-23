from django.db import IntegrityError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles import models
from doctor_profiles import serializers
from rest_framework import viewsets, permissions, status

from doctor_profiles.models import DoctorProfile, MedicalInstitution, DoctorQuestionnaire, Questionnaire


class QuestionnaireWritePermissionsMixin(object):
    def get_queryset(self):
        queryset = super(QuestionnaireWritePermissionsMixin, self).get_queryset()
        user = self.request.user

        queryset = queryset.filter(created_by=user.base_profile())

        return queryset


#############################################################################
# API Views
#############################################################################

class ApiQuestionnairePublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Questionnaire.objects.filter(restriction='public', is_approved=True)
    serializer_class = serializers.QuestionnairePublicSerializer
    permission_classes = [permissions.AllowAny]


class ApiQuestionnairePrivateViewSet(QuestionnaireWritePermissionsMixin, viewsets.ModelViewSet):
    queryset = models.Questionnaire.objects.all()
    serializer_class = serializers.QuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApiDoctorQuestionnairePublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.DoctorQuestionnairePublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs.get('doctor_id', None))
        if "medical_institution_id" in self.kwargs:
            medical_institution = get_object_or_404(MedicalInstitution, pk=self.kwargs.get('medical_institution'))
            return doctor.get_questionnaires(medical_institution=medical_institution)
        return doctor.get_questionnaires()


class ApiDoctorQuestionnairePrivateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DoctorQuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs.get('doctor_id', None))
        pk = self.kwargs.get('pk', None)
        filters = {}
        if pk:
            filters["pk"] = pk
        if "medical_institution_id" in self.request.GET:
            medical_institution = get_object_or_404(MedicalInstitution, pk=self.request.GET.get('medical_institution'))
            filters["medical_institution"] = medical_institution
        return doctor.get_questionnaires_rel(**filters)

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs.get('doctor_id', None))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result, message = doctor.add_questionnaire(
                **serializer.validated_data
            )
            if result:
                return Response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        rel = get_object_or_404(DoctorQuestionnaire, pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance=rel, data=request.data)
        if serializer.is_valid():
            obj = DoctorQuestionnaire.objects.update(
                **serializer.validated_data
            )
            if obj:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Oops", status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiQuestionnaireSectionPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionnaireSectionPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs.get('questionnaire_id', None), restriction='public')
        return questionnaire.get_sections()


#############################################################################
# Viewsets
#############################################################################

class QuestionnaireViewSet(viewsets.ModelViewSet):
    """ViewSet for the Questionnaire class"""

    queryset = models.Questionnaire.objects.all()
    serializer_class = serializers.QuestionnaireSerializer
    permission_classes = [permissions.IsAdminUser]


class DoctorQuestionnaireViewSet(viewsets.ModelViewSet):
    """ViewSet for the DoctorQuestionnaire class"""

    queryset = models.DoctorQuestionnaire.objects.all()
    serializer_class = serializers.DoctorQuestionnaireSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionnaireSectionViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionnaireSection class"""

    queryset = models.QuestionnaireSection.objects.all()
    serializer_class = serializers.QuestionnaireSectionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Question class"""

    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class SectionQuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the SectionQuestion class"""

    queryset = models.SectionQuestion.objects.all()
    serializer_class = serializers.SectionQuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class ChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Choice class"""

    queryset = models.Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]


class ChoiceGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChoiceGroup class"""

    queryset = models.ChoiceGroup.objects.all()
    serializer_class = serializers.ChoiceGroupSerializer
    permission_classes = [permissions.IsAdminUser]


class ChoiceGroupItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChoiceGroupItem class"""

    queryset = models.ChoiceGroupItem.objects.all()
    serializer_class = serializers.ChoiceGroupItemSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionChoiceGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionChoiceGroup class"""

    queryset = models.QuestionChoiceGroup.objects.all()
    serializer_class = serializers.QuestionChoiceGroupSerializer
    permission_classes = [permissions.IsAdminUser]
