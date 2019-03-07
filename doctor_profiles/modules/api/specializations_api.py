"""
- Specialization
--- ApiPublicSpecializationList - done
--- ApiPublicSpecializationDetail - done
--- ApiPrivateSpecializationCreate - done

- DoctorSpecialization
--- ApiPublicDoctorSpecializationList - done
--- ApiPublicDoctorSpecializationDetail - done
--- ApiPrivateDoctorSpecializationDetail - done
--- ApiPrivateDoctorSpecializationCreate - done
--- ApiPrivateDoctorSpecializationUpdate - done
--- ApiPrivateDoctorSpecializationDelete - done
"""
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import Specialization, DoctorSpecialization
from doctor_profiles.serializers import (
    SpecializationPublicSerializer,
    SpecializationCreateSerializer,
    DoctorSpecializationSerializer,
    DoctorSpecializationPublicSerializer,
    DoctorSpecializationCreateSerializer,
    DoctorSpecializationUpdateSerializer,
)


class ApiPublicSpecializationList(APIView):
    """
    Get list of all approved Specializations
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        specializations = Specialization.objects.filter(
            is_approved=True, parent__isnull=True
        )
        serializer = SpecializationPublicSerializer(specializations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicSpecializationDetail(APIView):
    """
    Get specific Specialization
    ?id=id or ?slug=slug
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id", None)
        slug = request.GET.get("slug", None)
        if id is not None:
            try:
                specialization = Specialization.objects.get(id=id, is_approved=True)
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
            serializer = SpecializationPublicSerializer(specialization)
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
            return Response(
                "Only Doctors can perform this action",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = SpecializationCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


################################################################################
# DoctorSpecialization
################################################################################


class ApiPublicDoctorSpecializationList(APIView):
    """
    Get Specializations of doctor profile
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, id=request.GET.get("user", None))
        if user.doctor_profile():
            specializations = user.doctor_profile().get_specializations_rel()
            serializer = DoctorSpecializationSerializer(specializations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                "User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND
            )


class ApiPrivateDoctorSpecializationDetail(APIView):
    """
    Detail of Medical Specialization of doctor profile
    ?specialization=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_specialization = get_object_or_404(
            DoctorSpecialization,
            id=request.GET.get("specialization", None),
            doctor=request.user.doctorprofile,
        )

        serializer = DoctorSpecializationSerializer(doctor_specialization)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicDoctorSpecializationDetail(APIView):
    """
    Public details of Medical Specialization
    ?specialization=id
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor_specialization = get_object_or_404(
            DoctorSpecialization, id=request.GET.get("specialization", None)
        )

        serializer = DoctorSpecializationPublicSerializer(doctor_specialization)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateDoctorSpecializationCreate(APIView):
    """
    Add Specialization to doctor profile
    ?user=n
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.doctor_profile():
            serializer = DoctorSpecializationCreateSerializer(data=request.data)

            if serializer.is_valid():
                doctor_specialization_kwargs = serializer.validated_data
                doctor_specialization_kwargs["doctor"] = user.doctor_profile()

                doctor_specialization = DoctorSpecialization(
                    **doctor_specialization_kwargs
                )
                try:
                    doctor_specialization.save()
                except IntegrityError:
                    return Response(
                        {
                            "Duplicate Medical Specialization": "You already have this medical specialization!"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ValueError as err:
                    return Response(
                        {"Value Error": str(err)}, status=status.HTTP_400_BAD_REQUEST
                    )
                return_serializer = DoctorSpecializationSerializer(
                    doctor_specialization
                )
                return Response(return_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND
            )


class ApiPrivateDoctorSpecializationUpdate(APIView):
    """
    Updates Medical Specialization of doctor profile
    ?specialization=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_specialization = get_object_or_404(
            DoctorSpecialization,
            id=request.GET.get("specialization", None),
            doctor=request.user.doctorprofile,
        )

        serializer = DoctorSpecializationUpdateSerializer(data=request.data)

        if serializer.is_valid():
            doctor_specialization.place_of_residency = serializer.validated_data[
                "place_of_residency"
            ]
            doctor_specialization.year_attained = serializer.validated_data[
                "year_attained"
            ]
            doctor_specialization.save()
            return_serializer = DoctorSpecializationSerializer(doctor_specialization)
            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ApiPrivateDoctorSpecializationDelete(APIView):
    """
    Deletes Medical Specialization of doctor profile
    ?specialization=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_specialization = get_object_or_404(
            DoctorSpecialization,
            id=request.GET.get("specialization", None),
            doctor=request.user.doctorprofile,
        )

        doctor_specialization.delete()
        return Response("Specialization deleted", status=status.HTTP_200_OK)
