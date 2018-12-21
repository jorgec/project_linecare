from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from drug_information.models import Drug
from drug_information.serializers.drug_serializers import DrugSerializer




class ApiPrivatePrescriptionCreate(APIView):
    """
    Add a new prescription
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # serializer = PrescriptionCreateSerializer(data=request.data)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass


class ApiPrivatePatientPrescriptionList(APIView):
    """
    Load prescriptions from checkup
    ?checkup_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        # serializer = PatientPrescriptionSerializer(checkup.get_prescriptions(), many=True)
        #
        # return Response(serializer.data, status=status.HTTP_200_OK)
        pass


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


class ApiPrivatePatientPrescriptionCreate(APIView):
    """
    Attach prescription to patient
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # serializer = PatientPrescriptionCreateSerializer(data=request.data)
        # if serializer.is_valid():
        #     checkup = serializer.validated_data['checkup']
        #     doctor = request.user.doctor_profile()
        #     if not doctor:
        #         return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        #     if not checkup.doctor_has_access(doctor):
        #         return Response(f"{doctor} does not have access privileges for this record",
        #                         status=status.HTTP_403_FORBIDDEN)
        #
        #     try:
        #         patient_prescriptions = PatientPrescription.objects.create(
        #             added_by=doctor,
        #             prescription=serializer.validated_data.get('prescription'),
        #             checkup=serializer.validated_data.get('checkup')
        #         )
        #     except IntegrityError:
        #         return Response("That prescription has already been added! If you don't see it, check the dismissed list.",
        #                         status=status.HTTP_409_CONFLICT)
        #
        #     response_serializer = PatientPrescriptionSerializer(patient_prescriptions)
        #
        #     return Response(response_serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
