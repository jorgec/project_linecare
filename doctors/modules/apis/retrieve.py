from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from doctors.models import DoctorProfile


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

        user = get_object_or_404(DoctorProfile, pk=pk)

        doctor = '' #template

        return Response(doctor, status=status.HTTP_200_OK)
