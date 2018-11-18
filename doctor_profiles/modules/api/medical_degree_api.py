from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import MedicalDegree, DoctorDegree
from doctor_profiles.serializers import MedicalDegreeCreateSerializer, MedicalDegreeSerializer, DoctorDegreeSerializer, \
    DoctorDegreeCreateSerializer, DoctorDegreeEditSerializer


class ApiPrivateMedicalDegreeAdd(APIView):
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


class ApiPublicMedicalDegreeDetail(APIView):
    """
    Medical Degree detail
    ?pk=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_degree = get_object_or_404(MedicalDegree, pk=request.GET.get('pk', None))
        serializer = MedicalDegreeSerializer(medical_degree)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicGetMedicalDegrees(APIView):
    """
    Get list of all approved Medical Degrees
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_degrees = MedicalDegree.objects.filter(is_approved=True)
        serializer = MedicalDegreeSerializer(medical_degrees, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicGetMedicalDegree(APIView):
    """
    Get specific Medical Degree
    ?pk=n or ?slug=s
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        slug = request.GET.get('slug', None)
        if pk is not None:
            try:
                medical_degree = MedicalDegree.objects.get(pk=pk)
            except MedicalDegree.DoesNotExist:
                medical_degree = None
        elif slug is not None:
            try:
                medical_degree = MedicalDegree.objects.get(slug=slug)
            except MedicalDegree.DoesNotExist:
                medical_degree = None
        else:
            medical_degree = None

        if medical_degree is not None:
            serializer = MedicalDegreeSerializer(medical_degree)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


""" Doctor Degree """


class ApiPublicGetDoctorDegrees(APIView):
    """
    Get Medical Degrees of doctor profile
    ?user=n
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, pk=request.GET.get('user', None))
        if user.doctor_profile():
            degrees = user.doctor_profile().get_degrees()
            serializer = DoctorDegreeSerializer(degrees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND)


class ApiPrivateDoctorDegreeAdd(APIView):
    """
    Add Medical Degree to doctor profile
    ?user=n
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(Account, pk=request.GET.get('user', None))
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


class ApiPrivateDoctorDegreeEdit(APIView):
    """
    Edits Medical Degree of doctor profile
    ?degree=pk
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, pk=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        serializer = DoctorDegreeEditSerializer(data=request.data)

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
    ?degree=pk
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, pk=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        doctor_degree.delete()
        return Response("Degree deleted", status=status.HTTP_200_OK)


class ApiPrivateDoctorDegreeDetail(APIView):
    """
    Detail of Medical Degree of doctor profile
    ?degree=pk
    """

    def get(self, request, *args, **kwargs):
        doctor_degree = get_object_or_404(DoctorDegree, pk=request.GET.get('degree', None),
                                          doctor=request.user.doctorprofile)

        serializer = DoctorDegreeSerializer(doctor_degree)
        return Response(serializer.data, status=status.HTTP_200_OK)
