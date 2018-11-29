from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


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
