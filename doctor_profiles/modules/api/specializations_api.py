"""
- Specialization
--- ApiPublicSpecializationList
--- ApiPublicSpecializationDetail
--- ApiPrivateSpecializationCreate

- DoctorSpecialization
--- ApiPublicDoctorSpecializationList
--- ApiPublicDoctorSpecializationDetail
--- ApiPrivateDoctorSpecializationDetail
--- ApiPrivateDoctorSpecializationCreate
--- ApiPrivateDoctorSpecializationEdit
--- ApiPrivateDoctorSpecializationDelete
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import Specialization
from doctor_profiles.serializers import SpecializationSerializer, SpecializationCreateSerializer


class ApiPublicSpecializationList(APIView):
    """
    Get list of all approved Specializations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        specializations = Specialization.objects.filter(is_approved=True, parent__isnull=True)
        serializer = SpecializationSerializer(specializations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicSpecializationDetail(APIView):
    """
    Get specific Specialization
    ?pk=pk or ?slug=slug
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        slug = request.GET.get('slug', None)
        if pk is not None:
            try:
                specialization = Specialization.objects.get(pk=pk, is_approved=True)
            except Specialization.DoesNotExist:
                specialization = None
        elif slug is not None:
            try:
                specialization = Specialization.objects.get(slug=slug, is_approved=True)
            except Specialization.DoesNotExist:
                specialization = None
        else:
            specialization = None

        if specialization is not None:
            serializer = SpecializationSerializer(specialization)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ApiPrivateSpecializationCreate(APIView):
    """
    Create Specialization
    Requires doctor profile
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctor_profile():
            return Response("Only Doctors can perform this action", status=status.HTTP_401_UNAUTHORIZED)

        serializer = SpecializationCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
