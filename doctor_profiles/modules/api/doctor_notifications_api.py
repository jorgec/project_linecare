from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiPrivateDoctorAppointmentNotificationsList(APIView):
    """
    Get Doctor's appointment notifications
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Invalid profile", status=status.HTTP_401_UNAUTHORIZED)

        return Response(doctor.appointment_notifications(), status=status.HTTP_200_OK)


class ApiPrivateDoctorAppointmentNotificationsDelete(APIView):
    """
    Clear Doctor's appointment notifications
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Invalid profile", status=status.HTTP_401_UNAUTHORIZED)

        return Response(doctor.clear_appointment_notifications(), status=status.HTTP_200_OK)
