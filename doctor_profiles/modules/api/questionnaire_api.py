from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles import models
from doctor_profiles import serializers
from doctor_profiles.models import DoctorProfile, MedicalInstitution, DoctorQuestionnaire, Questionnaire, Question
from doctor_profiles.permissions import is_doctor_or_receptionist, user_is_authorized


class QuestionnaireWritePermissionsMixin(object):
    def get_queryset(self):
        queryset = super(QuestionnaireWritePermissionsMixin, self).get_queryset()
        user = self.request.user

        queryset = queryset.filter(created_by=user.base_profile())

        return queryset


class DoctorQuestionnaireAuthCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if "pk" in kwargs:
            rel = get_object_or_404(DoctorQuestionnaire, pk=kwargs.get('pk'))
            doctor = rel.doctor
        else:
            doctor = get_object_or_404(DoctorProfile, pk=kwargs.get('doctor_id', None))

        is_valid_profile, request_profile = is_doctor_or_receptionist(request.user)
        if not is_valid_profile:
            raise PermissionDenied

        is_authorized = user_is_authorized(user=request.user, doctor=doctor, allowed_types=['doctor', 'receptionist'])
        if not is_authorized:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


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
        pk = self.kwargs.get('pk', None)
        filters = {
            'questionnaire__restriction': 'public'
        }
        if pk:
            filters["pk"] = pk
        if "medical_institution_id" in self.request.GET:
            medical_institution = get_object_or_404(MedicalInstitution, pk=self.request.GET.get('medical_institution'))
            filters["medical_institution"] = medical_institution
        return doctor.get_questionnaires_rel(**filters)


class ApiDoctorQuestionnairePrivateViewSet(DoctorQuestionnaireAuthCheckMixin, viewsets.ModelViewSet):
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

        serializer = serializers.DoctorQuestionnaireCreateSerializer(data=request.data)
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
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Oops", status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        rel = get_object_or_404(DoctorQuestionnaire, pk=kwargs.get('pk'))

        serializer = serializers.DoctorQuestionnaireDeleteSerializer(instance=rel, data=request.data)

        if serializer.is_valid():
            rel.delete()
            return Response(f"{rel} deleted", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiQuestionnaireSectionPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionnaireSectionPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs.get('questionnaire_id', None),
                                          restriction='public')
        index = self.kwargs.get('index', None)
        if index:
            return questionnaire.section(index)
        else:
            return questionnaire.get_sections()


class ApiQuestionnaireSectionPrivateViewSet(QuestionnaireWritePermissionsMixin, viewsets.ModelViewSet):
    serializer_class = serializers.QuestionnaireSectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs.get('questionnaire_id', None),
                                          created_by=self.request.user.base_profile())

        is_valid_profile, request_profile = is_doctor_or_receptionist(self.request.user)
        if not is_valid_profile:
            return None

        index = self.kwargs.get('index', None)
        if index:
            return questionnaire.section(index)
        else:
            return questionnaire.get_sections()

    def retrieve(self, request, *args, **kwargs):
        index = self.kwargs.get('index', None)
        questionnaire = get_object_or_404(Questionnaire, pk=kwargs.get('questionnaire_id', None),
                                          restriction='public')
        if not index:
            return Response("No index supplied", status=status.HTTP_400_BAD_REQUEST)

        try:
            section = questionnaire.section(index)
            return Response(self.serializer_class(section).data, status=status.HTTP_200_OK)
        except IndexError:
            return Response("Out of bounds", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        index = self.kwargs.get('index', None)
        questionnaire = get_object_or_404(Questionnaire, pk=kwargs.get('questionnaire_id', None),
                                          restriction='public')
        if not index:
            return Response("No index supplied", status=status.HTTP_400_BAD_REQUEST)

        section = questionnaire.section(index)

        serializer = self.serializer_class(instance=section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        index = self.kwargs.get('index', None)
        questionnaire = get_object_or_404(Questionnaire, pk=kwargs.get('questionnaire_id', None),
                                          restriction='public')
        if not index:
            return Response("No index supplied", status=status.HTTP_400_BAD_REQUEST)

        section = questionnaire.section(index)

        section.delete()
        return Response("Delete successful", status=status.HTTP_200_OK)


class ApiQuestionPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        filters = {
            'restriction': 'public',
            'is_approved': True
        }
        if pk:
            filters["pk"] = pk
        return Question.objects.filter(**filters)


class ApiQuestionPrivateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        filters = {
            'created_by': self.request.user.base_profile(),
            'is_approved': True
        }
        if pk:
            filters["pk"] = pk
        return Question.objects.filter(**filters)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.base_profile())

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.base_profile())


class ApiQuestionSearchPrivateView(APIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        if s:
            result = Question.objects.filter(
                Q(
                    Q(name__icontains=s) |
                    Q(text__icontains=s) |
                    Q(tags__name__in=[s])
                ) &
                Q(
                    Q(restriction='public') |
                    Q(created_by=request.user.base_profile())
                )
            )

            return Response(self.serializer_class(result, many=True).data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)


#############################################################################
# Admin ViewSets
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
