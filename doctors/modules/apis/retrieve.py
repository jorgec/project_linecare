from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.models import Account
from doctors.models import DoctorProfile
from doctors.modules.response_templates.profile import private_doctor_profile_template, public_doctor_profile_template


class ApiPrivateDoctorProfileGetByPK(APIView):
    """
    Get doctor's profile via PK
    ?pk=<pk>
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        doctor = private_doctor_profile_template(user)

        return Response(doctor, status=status.HTTP_200_OK)

class ApiPublicDoctorProfileGetByPK(APIView):
    """
    Get doctor's public profile via PK
    ?pk=<pk>
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        doctor = public_doctor_profile_template(user)

        return Response(doctor, status=status.HTTP_200_OK)

class ApiPublicDoctorProfileGetByMedicalSubject(APIView):
    """
    Get doctor's public profile via Medical Subject
    ?medical_subject=<medical_subject>
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_subject = request.GET.get('medical_subject', None)
        if not medical_subject:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        doctors = DoctorProfile.objects.filter(medical_subject=medical_subject)
        profiles = []
        for doctor in doctors:
            user = Account.objects.get(username = doctor.profile)
            user = public_doctor_profile_template(user)
            profiles.append(user)

        return Response(profiles, status=status.HTTP_200_OK)

class ApiPrivateDoctorProfileGetByMedicalSubject(APIView):
    """
    Get doctor's private profile via Medical Subject
    ?medical_subject=<medical_subject>
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medical_subject = request.GET.get('medical_subject', None)
        if not medical_subject:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        doctors = DoctorProfile.objects.filter(medical_subject=medical_subject)
        profiles = []
        for doctor in doctors:
            user = Account.objects.get(username=doctor.profile)
            user = private_doctor_profile_template(user)
            profiles.append(user)

        return Response(profiles, status=status.HTTP_200_OK)