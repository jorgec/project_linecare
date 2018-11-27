from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import DoctorProfile, MedicalInstitution
from profiles.models import BaseProfile
from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.serializers import ReceptionistProfileCreateByDoctorSerializer, ReceptionistProfileSerializer


class ApiPrivateReceptionistProfileCreateByDoctor(APIView):
    """
    Create a receptionist profile for someone via a doctor account
    ?doctor_id=doctor_id&medical_institution_id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution_id', None))

        serializer = ReceptionistProfileCreateByDoctorSerializer(data=request.data)

        if serializer.is_valid():

            account = Account.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            profile = account.base_profile()
            profile.first_name = serializer.validated_data['first_name']
            profile.last_name = serializer.validated_data['last_name']
            profile.is_fresh = False
            profile.save()

            receptionist = ReceptionistProfile.objects.create_by_doctor(
                doctor=doctor,
                medical_institution=medical_institution,
                user=account
            )

            return_serializer = ReceptionistProfileSerializer(receptionist)

            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
