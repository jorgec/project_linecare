from rest_framework import status, permissions, parsers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.constants import APPOINTMENT_TYPES
from doctor_profiles.models import DoctorProfile
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from receptionist_profiles.models import ReceptionistProfile


def is_doctor_or_receptionist(user):
    user_type = None
    try:
        doctor = DoctorProfile.objects.get(user=user)
        user_type = doctor
    except DoctorProfile.DoesNotExist:
        try:
            receptionist = ReceptionistProfile.objects.get(user=user)
            user_type = receptionist
        except ReceptionistProfile.DoesNotExist:
            return False, user_type
    return True, user_type


class ApiMedicalInstitutionDoctorMetaList(APIView):
    """
    Get meta for connection; creates defaults if None
    ?id=rel_id&key=str
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        connection = get_object_or_404(
            MedicalInstitutionDoctor,
            is_approved=True,
            id=request.GET.get('id', None)
        )

        types = APPOINTMENT_TYPES

        if len(connection.metadata) == 0:
            connection.metadata['durations'] = {}
            connection.metadata['fees'] = {}
            for t in types:
                connection.metadata['durations'][f'{t[0]}_duration'] = 15
                connection.metadata['durations'][f'{t[0]}_gap'] = 1
                connection.metadata['fees'][t[0]] = 0
            connection.save()

        key = request.GET.get('key', None)
        if key:
            return Response(connection.metadata[key], status=status.HTTP_200_OK)

        return Response(connection.metadata, status=status.HTTP_200_OK)


class ApiMedicalInstitutionDoctorMetaUpdate(APIView):
    """
    Update connection meta
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        connection = get_object_or_404(
            MedicalInstitutionDoctor,
            is_approved=True,
            id=request.data.get('rel_id', None)
        )

        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        if type(profile_type) != DoctorProfile:
            """ person updating isn't the doctor, so check if receptionist is allowed """
            receptionist_connection = connection.doctor.verify_receptionist(
                receptionist=request.user.receptionistprofile,
                medical_institution=connection.medical_institution)
            if not receptionist_connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != connection.doctor.id:
            return Response("This is not your profile", status=status.HTTP_401_UNAUTHORIZED)

        key = request.data.get('key', None)

        if not key:
            return Response("Invalid metadata key", status=status.HTTP_400_BAD_REQUEST)

        for k, data in request.data.items():
            if k.startswith("payload__"):
                label = k.replace("payload__", "")
                connection.metadata[key][label] = data


        print(connection.metadata)

        connection.save()
        return Response(connection.metadata, status=status.HTTP_200_OK)
