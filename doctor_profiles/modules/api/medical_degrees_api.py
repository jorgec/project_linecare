"""
- MedicalDegree
--- ApiPublicMedicalDegreeList
--- ApiPublicMedicalDegreeDetail
--- ApiPrivateMedicalDegreeCreate

- DoctorDegree
--- ApiPublicDoctorDegreeList
--- ApiPublicDoctorDegreeDetail
--- ApiPrivateDoctorDegreeDetail
--- ApiPrivateDoctorDegreeCreate
--- ApiPrivateDoctorDegreeUpdate
--- ApiPrivateDoctorDegreeDelete
"""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import MedicalDegree, DoctorDegree
from doctor_profiles.serializers import MedicalDegreeCreateSerializer, MedicalDegreePublicSerializer, \
    DoctorDegreeSerializer, DoctorDegreeCreateSerializer, DoctorDegreeUpdateSerializer, DoctorDegreePublicSerializer


class ApiPrivateMedicalDegreeCreate(APIView):
    """
    Create Medical Degree
    Requires doctor profile
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctor_profile():
            return Response("Only Doctors can perform this action", status=status.HTTP_401_UNAUTHORIZED)

        serializer = MedicalDegreeCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicMedicalDegreeList(APIView):
    """
    Get list of all approved Medical Degrees
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_degrees = MedicalDegree.objects.filter(is_approved=True)
        serializer = MedicalDegreePublicSerializer(medical_degrees, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalDegreeDetail(APIView):
    """
    Get specific Medical Degree
    ?id=id or ?slug=slug
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        slug = request.GET.get('slug', None)
        if id is not None:
            try:
                medical_degree = MedicalDegree.objects.get(id=id, is_approved=True)
            except MedicalDegree.DoesNotExist:
                medical_degree = None
        elif slug is not None:
            try:
                medical_degree = MedicalDegree.objects.get(slug=slug, is_approved=True)
            except MedicalDegree.DoesNotExist:
                medical_degree = None
        else:
            medical_degree = None

        if medical_degree is not None:
            serializer = MedicalDegreePublicSerializer(medical_degree)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


################################################################################
# Doctor Degree
################################################################################


class ApiPublicDoctorDegreeList(APIView):
    """
    Get Medical Degrees of doctor profile
    ?user=n
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, id=request.GET.get('user', None))
        if user.doctor_profile():
            degrees = user.doctor_profile().get_degrees_rel()
            serializer = DoctorDegreeSerializer(degrees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND)


class ApiPrivateDoctorDegreeCreate(APIView):
    """
    Create Medical Degree to doctor profile
    ?user=n
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.doctor_profile():
            serializer = DoctorDegreeCreateSerializer(data=request.data)

            if serializer.is_valid():
                doctor_degree_kwargs = serializer.validated_data
                doctor_degree_kwargs['doctor'] = user.doctor_profile()

                private_license = request.data.get('private_license', None)
                if private_license:
                    doctor_degree_kwargs['metadata'] = {
                        'private_license': True
                    }

                doctor_degree = DoctorDegree(**doctor_degree_kwargs)
                try:
                    doctor_degree.save()
                except IntegrityError:
                    return Response(
                        {
                            "Duplicate Medical Degree": "You already have this medical degree!"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except ValueError as err:
                    return Response(
                        {
                            "Value Error": str(err)
                        }, status=status.HTTP_400_BAD_REQUEST)
                return_serializer = DoctorDegreeSerializer(doctor_degree)
                return Response(return_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND)


class ApiPrivateDoctorDegreeUpdate(APIView):
    """
    Updates Medical Degree of doctor profile
    ?degree=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, id=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        serializer = DoctorDegreeUpdateSerializer(data=request.data)

        if serializer.is_valid():
            doctor_degree.school = serializer.validated_data['school']
            doctor_degree.year_attained = serializer.validated_data['year_attained']
            doctor_degree.license_number = serializer.validated_data['license_number']
            doctor_degree.save()
            return_serializer = DoctorDegreeSerializer(doctor_degree)
            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ApiPrivateDoctorDegreeDelete(APIView):
    """
    Deletes Medical Degree of doctor profile
    ?degree=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, id=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        doctor_degree.delete()
        return Response("Degree deleted", status=status.HTTP_200_OK)


class ApiPrivateDoctorDegreeDetail(APIView):
    """
    Detail of Medical Degree of doctor profile
    ?degree=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, id=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        serializer = DoctorDegreeSerializer(doctor_degree)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicDoctorDegreeDetail(APIView):
    """
    Public details of Medical Degree
    ?degree=id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, id=request.GET.get('degree', None))

        serializer = DoctorDegreePublicSerializer(doctor_degree)
        return Response(serializer.data, status=status.HTTP_200_OK)
