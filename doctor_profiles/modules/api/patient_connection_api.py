from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import DoctorProfile, PatientConnection
from doctor_profiles.serializers.patient_connection_serializers import PatientConnectionDoctorViewSerializer
from profiles.serializers import BaseProfilePrivateSerializerFull
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


class ApiPrivatePatientConnectionSearchList(APIView):
    """
    Get preexisting patient connections
    ?doctor_id=doctor_id
    [optional]
    &s=str
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response(
                "Incompatible user profile", status=status.HTTP_403_FORBIDDEN
            )

        doctor_id = request.GET.get("doctor_id", None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        s = request.GET.get("s", None)

        if type(profile_type) != DoctorProfile:
            """ person accessing isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(
                receptionist=request.user.receptionistprofile
            )
            if not connection:
                return Response(
                    "Receptionist is not authorized by this doctor for this medical institution",
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif profile_type.id != doctor.id:
            return Response(
                "Your magic has no power here!", status=status.HTTP_401_UNAUTHORIZED
            )

        filters = {"doctor": doctor}

        if s:
            qs = PatientConnection.objects.annotate(
                fullname=Concat("patient__first_name", Value(" "), "patient__last_name")
            ).filter(**filters)
            connections = qs.filter(
                Q(patient__last_name__icontains=s)
                | Q(patient__first_name__icontains=s)
                | Q(fullname__icontains=s)
            ).order_by("patient__fullname")
        else:
            connections = PatientConnection.objects.filter(**filters).order_by(
                "patient__fullname"
            )

        serializer = PatientConnectionDoctorViewSerializer(connections, many=True)
        # patients = {c.patient for c in connections}
        # serializer = BaseProfilePrivateSerializerFull(patients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
