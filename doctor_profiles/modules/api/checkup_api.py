from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import PatientCheckupRecord, CheckupNote
from doctor_profiles.serializers.checkup_serializers import CheckupNoteSerializer, CheckupNoteCreateSerializer


class ApiCheckupNoteList(APIView):
    """
    Get notes from checkup
    ?checkup_id=checkup_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)

        notes = CheckupNote.objects.filter(checkup=checkup)

        serializer = CheckupNoteSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiCheckupNoteCreate(APIView):
    """
    Add note to checkup
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        checkup = get_object_or_404(PatientCheckupRecord, id=request.GET.get('checkup_id', None))
        doctor = request.user.doctor_profile()
        if not doctor:
            return Response("Not a doctor", status=status.HTTP_401_UNAUTHORIZED)
        if not checkup.doctor_has_access(doctor):
            return Response(f"{doctor} does not have access privileges for this record",
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CheckupNoteCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response("Note added", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
