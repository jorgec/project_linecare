from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.serializers import ReceptionistConnectionPrivateNestedSerializer


class ApiPrivateReceptionistProfileConnectionList(APIView):
    """
    Get connected doctors and medical institutions
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.receptionistprofile:
            return Response("Not a receptionist", status=status.HTTP_401_UNAUTHORIZED)
        receptionist = get_object_or_404(ReceptionistProfile, id=request.user.receptionistprofile.id)

        serializer = ReceptionistConnectionPrivateNestedSerializer(receptionist.get_medical_institution_connections(),
                                                                   many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
