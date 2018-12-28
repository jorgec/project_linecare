from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import PatientCheckupRecord
from doctor_profiles.models.patient_checkup_models import Prescription
from doctor_profiles.serializers.prescription_serializers import PrescriptionCreateSerializer, \
    PatientPrescriptionSerializer


class ApiPrivatePrescriptionCreate(APIView):
    """
    Add a new prescription
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)

        if serializer.is_valid():
            checkup = serializer.validated_data['checkup']
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass


class ApiPrivatePatientPrescriptionList(APIView):
    """
    Load prescriptions from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))

        if request.user != checkup.appointment.patient:
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

        serializer = PatientPrescriptionSerializer(checkup.get_prescriptions(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientPrescriptionDetail(APIView):
    """
    Prescription detail
    ?id=prescription_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        prescription = get_object_or_404(Prescription, id=request.GET.get('id', None))
        checkup = prescription.checkup

        if request.user != checkup.appointment.patient:
            doctor = request.user.doctor_profile()
            if not doctor:
                return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
            if not checkup.doctor_has_access(doctor):
                return Response(f"{doctor} does not have access privileges for this record",
                                status=status.HTTP_403_FORBIDDEN)

        serializer = PatientPrescriptionSerializer(prescription)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientDismissedPrescriptionList(APIView):
    """
    Load dismissed prescriptions from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        # serializer = PatientPrescriptionSerializer(checkup.get_dismissed_prescriptions(), many=True)
        #
        # return Response(serializer.data, status=status.HTTP_200_OK)
        pass


class ApiPrivatePatientPrescriptionRemove(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # patient_prescription = get_object_or_404(PatientPrescription, prescription_id=request.GET.get('id', None),
        #                                     checkup_id=request.GET.get('checkup_id'))
        # doctor = request.user.doctor_profile()
        # if not doctor:
        #     return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        # if not patient_prescription.checkup.doctor_has_access(doctor):
        #     return Response(f"{doctor} does not have access privileges for this record",
        #                     status=status.HTTP_403_FORBIDDEN)
        #
        # patient_prescription.is_deleted = True
        # patient_prescription.removed_by = doctor
        # patient_prescription.save()
        # response_serializer = PatientPrescriptionSerializer(patient_prescription)
        # return Response(response_serializer.data, status=status.HTTP_200_OK)
        pass
