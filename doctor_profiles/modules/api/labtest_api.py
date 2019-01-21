from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import LabTest, PatientLabTestRequest, PatientCheckupRecord
from doctor_profiles.serializers.labtest_serializers import LabTestSerializer, PatientLabTestRequestSerializer, \
    PatientLabTestRequestCreateSerializer


class ApiPublicLabtestList(APIView):
    """
    List lab tests
    [optional]
    ?s=str
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)

        if s:
            labtests = LabTest.objects.annotate(
                search=SearchVector(
                    'description',
                    'purpose',
                    'indication',
                    'usage',
                )
            ).filter(
                Q(search=s) |
                Q(name__icontains=s) |
                Q(aliases__icontains=s)
            )
        else:
            labtests = LabTest.objects.all()

        serializer = LabTestSerializer(labtests, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class ApiPrivatePatientLabTestCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PatientLabTestRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            checkup = serializer.validated_data['checkup']
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

            try:
                patient_labtest = PatientLabTestRequest.objects.create(
                    requested_by=doctor,
                    lab_test=serializer.validated_data.get('lab_test'),
                    checkup=serializer.validated_data.get('checkup')
                )

            except IntegrityError:
                return Response("That test has already been requested.",
                                status=status.HTTP_409_CONFLICT)

            response_serializer = PatientLabTestRequestSerializer(patient_labtest)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientLabTestList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PatientLabTestRequestSerializer(checkup.get_requested_tests(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDismissedLabTestList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PatientLabTestRequestSerializer(checkup.get_dismissed_tests(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApiPrivatePatientLabTestRemove(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_labtest = get_object_or_404(PatientLabTestRequest, lab_test_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not patient_labtest.checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)

        patient_labtest.is_approved = False
        patient_labtest.removed_by = doctor
        patient_labtest.save()
        response_serializer = PatientLabTestRequestSerializer(patient_labtest)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientLabTestUndismiss(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient_labtest = get_object_or_404(PatientLabTestRequest, lab_test_id=request.GET.get('id', None),
                                            checkup_id=request.GET.get('checkup_id'))
        doctor = request.user.doctor_profile()

        if patient_labtest.removed_by == doctor:
            patient_labtest.is_approved = True
            patient_labtest.removed_by = None
            patient_labtest.save()
            response_serializer = PatientLabTestRequestSerializer(patient_labtest)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"Only {patient_labtest.removed_by} can undismiss this entry",
                            status=status.HTTP_403_FORBIDDEN)
