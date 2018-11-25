from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


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
