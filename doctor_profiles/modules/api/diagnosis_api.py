from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import Diagnosis, PatientCheckupRecord, PatientDiagnosis
from doctor_profiles.serializers.diagnosis_serializers import (
    Diagnoseserializer,
    DiagnosisCreateSerializer,
    PatientDiagnosisCreateSerializer,
    PatientDiagnoseserializer,
)


class ApiPublicDiagnosisList(APIView):
    """
    List of diagnoses
    [optional]
    ?s=str
    ?page=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get("s", None)
        page = request.GET.get("page", None)
        if s:
            diagnoses = Diagnosis.objects.annotate(
                search=SearchVector("name", "description")
            ).filter(search__icontains=s)
        else:
            diagnoses = Diagnosis.objects.all()

        if not page:
            diagnoses = diagnoses[:10]
        else:
            start = page * 10
            end = start + 10
            diagnoses = diagnoses[start:end]

        serializer = Diagnoseserializer(diagnoses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateDiagnosisCreate(APIView):
    """
    Add a new diagnosis
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DiagnosisCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientDiagnosisList(APIView):
    """
    Load diagnoses from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(
            PatientCheckupRecord, id=request.GET.get("checkup_id", None)
        )
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(
                f"{doctor} does not have access privileges for this record",
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = PatientDiagnoseserializer(checkup.get_diagnoses(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDismissedDiagnosisList(APIView):
    """
    Load dismissed diagnoses from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(
            PatientCheckupRecord, id=request.GET.get("checkup_id", None)
        )
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(
                f"{doctor} does not have access privileges for this record",
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PatientDiagnoseserializer(
            checkup.get_dismissed_diagnoses(), many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDiagnosisCreate(APIView):
    """
    Attach diagnosis to patient
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PatientDiagnosisCreateSerializer(data=request.data)
        if serializer.is_valid():
            checkup = serializer.validated_data["checkup"]
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(
                    f"{doctor} does not have access privileges for this record",
                    status=status.HTTP_403_FORBIDDEN,
                )

            try:
                patient_diagnoses = PatientDiagnosis.objects.create(
                    added_by=doctor,
                    diagnosis=serializer.validated_data.get("diagnosis"),
                    checkup=serializer.validated_data.get("checkup"),
                )
            except IntegrityError:
                return Response(
                    "That diagnosis has already been added! If you don't see it, check the dismissed list.",
                    status=status.HTTP_409_CONFLICT,
                )

            response_serializer = PatientDiagnoseserializer(patient_diagnoses)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientDiagnosisRemove(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_diagnosis = get_object_or_404(
            PatientDiagnosis,
            diagnosis_id=request.GET.get("id", None),
            checkup_id=request.GET.get("checkup_id"),
        )
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not patient_diagnosis.checkup.doctor_has_access(doctor):
            return Response(
                f"{doctor} does not have access privileges for this record",
                status=status.HTTP_403_FORBIDDEN,
            )

        patient_diagnosis.is_deleted = True
        patient_diagnosis.removed_by = doctor
        patient_diagnosis.save()
        response_serializer = PatientDiagnoseserializer(patient_diagnosis)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDiagnosisUndismiss(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_diagnosis = get_object_or_404(
            PatientDiagnosis,
            diagnosis_id=request.GET.get("id", None),
            checkup_id=request.GET.get("checkup_id"),
        )
        doctor = request.user.doctor_profile()

        if patient_diagnosis.removed_by == doctor:
            patient_diagnosis.is_deleted = False
            patient_diagnosis.removed_by = None
            patient_diagnosis.save()
            response_serializer = PatientDiagnoseserializer(patient_diagnosis)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                f"Only {patient_diagnosis.removed_by} can undismiss this entry",
                status=status.HTTP_403_FORBIDDEN,
            )
