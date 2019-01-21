from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import Finding, PatientCheckupRecord, PatientFinding
from doctor_profiles.serializers.finding_serializers import FindingSerializer, FindingCreateSerializer, \
    PatientFindingCreateSerializer, PatientFindingSerializer


class ApiPublicFindingList(APIView):
    """
    List of findings
    [optional]
    ?s=str
    ?page=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        page = request.GET.get('page', None)
        if s:
            findings = Finding.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(search__icontains=s)
        else:
            findings = Finding.objects.all()

        if not page:
            findings = findings[:10]
        else:
            start = page * 10
            end = start + 10
            findings = findings[start:end]

        serializer = FindingSerializer(findings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateFindingCreate(APIView):
    """
    Add a new finding
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FindingCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientFindingList(APIView):
    """
    Load findings from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        serializer = PatientFindingSerializer(checkup.get_findings(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDismissedFindingList(APIView):
    """
    Load dismissed findings from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        serializer = PatientFindingSerializer(checkup.get_dismissed_findings(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientFindingCreate(APIView):
    """
    Attach finding to patient
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PatientFindingCreateSerializer(data=request.data)
        if serializer.is_valid():
            checkup = serializer.validated_data['checkup']
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

            try:
                patient_findings = PatientFinding.objects.create(
                    added_by=doctor,
                    finding=serializer.validated_data.get('finding'),
                    checkup=serializer.validated_data.get('checkup')
                )
            except IntegrityError:
                return Response("That finding has already been added! If you don't see it, check the dismissed list.",
                                status=status.HTTP_409_CONFLICT)

            response_serializer = PatientFindingSerializer(patient_findings)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientFindingRemove(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_finding = get_object_or_404(PatientFinding, finding_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not patient_finding.checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)

        patient_finding.is_deleted = True
        patient_finding.removed_by = doctor
        patient_finding.save()
        response_serializer = PatientFindingSerializer(patient_finding)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientFindingUndismiss(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_finding = get_object_or_404(PatientFinding, finding_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()

        if patient_finding.removed_by == doctor:
            patient_finding.is_deleted = False
            patient_finding.removed_by = None
            patient_finding.save()
            response_serializer = PatientFindingSerializer(patient_finding)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"Only {patient_finding.removed_by} can undismiss this entry",
                            status=status.HTTP_403_FORBIDDEN)
