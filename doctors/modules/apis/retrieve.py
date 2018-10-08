from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.models import Account
from doctors.modules.response_templates.profile import private_doctor_profile_template


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
