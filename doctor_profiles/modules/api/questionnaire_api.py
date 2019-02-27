from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles import models
from doctor_profiles import serializers
from doctor_profiles.models import DoctorProfile, MedicalInstitution, DoctorQuestionnaire, Questionnaire, Question, \
    SectionQuestion
from doctor_profiles.permissions import is_doctor_or_receptionist, user_is_authorized


def section_question_permissions_check(user, question, section):
    """
    check if question is either public, or:
        - if internal, request.user.doctor or request.user.receptionist is a member of medical institution
        - if private, owned by request.user.profile
    """
    question_allowed = False
    if question.restriction == 'public':
        question_allowed = question
    elif question.restriction == 'internal':
        mi_question_membership = []
        mi_user_membership = []
        if question.created_by.doctor_profile():
            mi_question_membership = question.created_by.doctor_profile().get_medical_institutions()
        elif question.created_by.receptionist_profile():
            mi_question_membership = question.created_by.receptionist_profile().get_medical_institutions_rel()

        if user.doctor_profile():
            mi_user_membership = user.doctor_profile().get_medical_institutions()
        elif user.receptionist_profile():
            mi_user_membership = user.receptionist_profile().get_medical_institutions_rel()

        if set(mi_question_membership).intersection(set(mi_user_membership)):
            question_allowed = question
    elif question.restriction == 'private':
        if question.created_by == user.base_profile():
            question_allowed = question

    """
    check if user is allowed to mess with the section
    """
    section_allowed = False
    if section.questionnaire.created_by == user.base_profile():
        section_allowed = section

    return section_allowed, question_allowed


class QuestionnaireWritePermissionsMixin(object):
    def get_queryset(self):
        queryset = super(QuestionnaireWritePermissionsMixin, self).get_queryset()
        user = self.request.user

        queryset = queryset.filter(created_by=user.base_profile(), is_approved=True)

        return queryset


class ChoiceGroupWritePermissionsMixin(object):
    def get_queryset(self):
        queryset = super(ChoiceGroupWritePermissionsMixin, self).get_queryset()
        user = self.request.user
        queryset = queryset.filter(choice_group__created_by=user.base_profile(), is_approved=True)
        return queryset


class QuestionChoiceGroupWritePermissionsMixin(object):
    def get_queryset(self):
        queryset = super(QuestionChoiceGroupWritePermissionsMixin, self).get_queryset()
        user = self.request.user
        queryset = queryset.filter(question__created_by=user.base_profile(), is_approved=True)
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

    def create(self, request, *args, **kwargs):
        serializer = serializers.QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data['created_by'] = self.request.user.base_profile()
            questionnaire = Questionnaire.objects.create_by_user(**data)
            return Response(self.serializer_class(questionnaire).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDoctorQuestionnairePublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.DoctorQuestionnairePublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs.get('doctor_id', None))
        pk = self.kwargs.get('pk', None)
        filters = {
            'questionnaire__restriction': 'public',
            'is_approved': True
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
        filters = {
            'is_approved': True
        }
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
                                          restriction='public', is_approved=True)
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
                                          created_by=self.request.user.base_profile(), is_approved=True)

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


class ApiQuestionPrivateViewSet(QuestionnaireWritePermissionsMixin, viewsets.ModelViewSet):
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
            ).filter(
                is_approved=True
            )

            return Response(self.serializer_class(result, many=True).data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)


class ApiSectionQuestionPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SectionQuestionPublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.SectionQuestion.objects.filter(section__questionnaire__restriction='public', is_approved=True)


class ApiSectionQuestionPrivateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SectionQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.SectionQuestion.objects.filter(
            section__questionnaire__created_by=self.request.user.base_profile()
        )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = serializers.SectionQuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            section_allowed, question_allowed = section_question_permissions_check(request.user,
                                                                                   serializer.validated_data.get(
                                                                                       'question'),
                                                                                   serializer.validated_data.get(
                                                                                       'section'))
            if question_allowed and section_allowed:
                section_question = SectionQuestion.objects.create(
                    order=serializer.validated_data.get('order'),
                    fork_map=serializer.validated_data.get('fork_map'),
                    question_flow=serializer.validated_data.get('question_flow'),
                    question=question_allowed,
                    section=section_allowed
                )
                created = self.serializer_class(section_question)
                return Response(created.data, status=status.HTTP_201_CREATED)

            return Response(f"Action forbidden; question: {question_allowed}; section: {section_allowed}",
                            status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"Duplicate question", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        section_question = SectionQuestion.objects.get(pk=kwargs.get('pk'))
        serializer = serializers.SectionQuestionUpdateSerializer(instance=section_question, data=request.data)
        if serializer.is_valid():
            section_allowed, question_allowed = section_question_permissions_check(request.user,
                                                                                   serializer.validated_data.get(
                                                                                       'question'),
                                                                                   serializer.validated_data.get(
                                                                                       'section'))
            if question_allowed and section_allowed:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response("Action forbidden", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        section_question = SectionQuestion.objects.get(pk=kwargs.get('pk'))
        section_allowed, question_allowed = section_question_permissions_check(request.user, section_question.question,
                                                                               section_question.section)
        if section_allowed:
            section_question.delete()
            return Response("Section question deleted!", status=status.HTTP_200_OK)
        return Response("Action forbidden", status=status.HTTP_403_FORBIDDEN)


class ApiChoicePublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ChoicePublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.Choice.objects.filter(is_approved=True)


class ApiChoicePrivateViewSet(QuestionnaireWritePermissionsMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Choice.objects.all()


class ApiChoiceGroupPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ChoiceGroupPublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.Choice.objects.filter(is_approved=True)


class ApiChoiceGroupPrivateViewSet(QuestionnaireWritePermissionsMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Choice.objects.all()


class ApiChoiceGroupItemPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ChoiceGroupItemPublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.ChoiceGroupItem.objects.filter(is_approved=True)


class ApiChoiceGroupItemPrivateViewSet(ChoiceGroupWritePermissionsMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceGroupItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.ChoiceGroupItem.objects.all()


class ApiQuestionChoiceGroupPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionChoiceGroupPublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.QuestionChoiceGroup.objects.filter(is_approved=True, question__restriction='public')


class ApiQuestionChoiceGroupPrivateViewSet(QuestionChoiceGroupWritePermissionsMixin, viewsets.ModelViewSet):
    serializer_class = serializers.QuestionChoiceGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.QuestionChoiceGroup.objects.all()


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
