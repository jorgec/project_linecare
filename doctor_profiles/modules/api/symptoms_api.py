from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import Symptom, PatientCheckupRecord, PatientSymptom
from doctor_profiles.serializers.symptom_serializers import SymptomSerializer, SymptomCreateSerializer, \
    PatientSymptomCreateSerializer, PatientSymptomSerializer


class ApiPublicSymptomList(APIView):
    """
    List of symptoms
    [optional]
    ?s=str
    ?page=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        page = request.GET.get('page', None)
        if s:
            symptoms = Symptom.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(search__icontains=s)
        else:
            symptoms = Symptom.objects.all()

        if not page:
            symptoms = symptoms[:10]
        else:
            start = page * 10
            end = start + 10
            symptoms = symptoms[start:end]

        serializer = SymptomSerializer(symptoms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateSymptomCreate(APIView):
    """
    Add a new symptom
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SymptomCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientSymptomList(APIView):
    """
    Load symptoms from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        serializer = PatientSymptomSerializer(checkup.get_symptoms(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDismissedSymptomList(APIView):
    """
    Load dismissed symptoms from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        serializer = PatientSymptomSerializer(checkup.get_dismissed_symptoms(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientSymptomCreate(APIView):
    """
    Attach symptom to patient
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PatientSymptomCreateSerializer(data=request.data)
        if serializer.is_valid():
            checkup = serializer.validated_data['checkup']
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

            try:
                patient_symptoms = PatientSymptom.objects.create(
                    added_by=doctor,
                    symptom=serializer.validated_data.get('symptom'),
                    checkup=serializer.validated_data.get('checkup')
                )
            except IntegrityError:
                return Response("That symptom has already been added! If you don't see it, check the dismissed list.",
                                status=status.HTTP_409_CONFLICT)

            response_serializer = PatientSymptomSerializer(patient_symptoms)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientSymptomRemove(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_symptom = get_object_or_404(PatientSymptom, symptom_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not patient_symptom.checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)

        patient_symptom.is_deleted = True
        patient_symptom.removed_by = doctor
        patient_symptom.save()
        response_serializer = PatientSymptomSerializer(patient_symptom)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientSymptomUndismiss(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_symptom = get_object_or_404(PatientSymptom, symptom_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()

        if patient_symptom.removed_by == doctor:
            patient_symptom.is_deleted = False
            patient_symptom.removed_by = None
            patient_symptom.save()
            response_serializer = PatientSymptomSerializer(patient_symptom)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"Only {patient_symptom.removed_by} can undismiss this entry",
                            status=status.HTTP_403_FORBIDDEN)
