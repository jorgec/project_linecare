"""
- Specialization
--- ApiPublicSpecializationList
--- ApiPublicSpecializationDetail
--- ApiPrivateSpecializationCreate

- DoctorSpecialization
--- ApiPublicDoctorSpecializationList
--- ApiPublicDoctorSpecializationDetail
--- ApiPrivateDoctorSpecializationDetail
--- ApiPrivateDoctorSpecializationCreate
--- ApiPrivateDoctorSpecializationEdit
--- ApiPrivateDoctorSpecializationDelete
"""
from rest_framework import permissions
from rest_framework.views import APIView

from doctor_profiles.models import Specialization


class ApiPublicSpecializationList(APIView):
    """
    Get list of all approved Specializations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        specializations = Specialization.objects.filter(is_approved=True, parent__isnull=True)