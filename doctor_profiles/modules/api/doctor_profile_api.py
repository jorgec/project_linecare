from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import DoctorProfile
from doctor_profiles.modules.response_templates.doctor_profile import public_doctor_profile_template
from doctor_profiles.serializers import MedicalInstitutionSerializer
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer, \
    DoctorProfilePublicSerializer


class ApiPrivateDoctorProfileCreate(APIView):
    """
    Create a doctor profile for user
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user.create_doctor_profile()

        serializer = DoctorProfilePrivateSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiDismissProfileProgressDisplay(APIView):
    """
    Dismiss showing of profile progress bar
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.doctor_profile():
            return Response("Only Doctors can perform this action", status=status.HTTP_401_UNAUTHORIZED)
        result = request.user.doctor_profile().dismiss_profile_progress_display()
        return Response(result, status=status.HTTP_200_OK)


class ApiPublicDoctorProfileDetail(APIView):
    """
    Get a doctor's public profile
    ?id=doctor_id
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('id', None))
        fmt = request.GET.get('fmt', 'full')

        if fmt == 'full':
            doctor_profile = public_doctor_profile_template(user=doctor.user)
        else:
            doctor_profile = DoctorProfilePublicSerializer(doctor).data

        return Response(doctor_profile, status=status.HTTP_200_OK)


class ApiPublicDoctorProfileMedicalInstitutions(APIView):
    """
    Get doctor's medical institutions
    ?id=doctor_id
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('id', None))

        serializer = MedicalInstitutionSerializer(doctor.get_medical_institutions(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
