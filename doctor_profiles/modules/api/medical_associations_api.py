"""
- MedicalAssociation
--- ApiPublicMedicalAssociationList
--- ApiPublicMedicalAssociationDetail
--- ApiPrivateMedicalAssociationCreate

- DoctorAssociation
--- ApiPublicDoctorAssociationList
--- ApiPublicDoctorAssociationDetail
--- ApiPrivateDoctorAssociationDetail
--- ApiPrivateDoctorAssociationCreate
--- ApiPrivateDoctorAssociationUpdate
--- ApiPrivateDoctorAssociationDelete
"""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import MedicalAssociation, DoctorAssociation
from doctor_profiles.serializers import (
    MedicalAssociationCreateSerializer,
    MedicalAssociationPublicSerializer,
    DoctorAssociationSerializer,
    DoctorAssociationCreateSerializer,
    DoctorAssociationUpdateSerializer,
    DoctorAssociationPublicSerializer,
)


class ApiPrivateMedicalAssociationCreate(APIView):
    """
    Create Medical Association
    Requires doctor profile
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctor_profile():
            return Response(
                "Only Doctors can perform this action",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = MedicalAssociationCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicMedicalAssociationList(APIView):
    """
    Get list of all approved Medical Associations
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_associations = MedicalAssociation.objects.filter(is_approved=True)
        serializer = MedicalAssociationPublicSerializer(medical_associations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalAssociationDetail(APIView):
    """
    Get specific Medical Association
    ?id=id or ?slug=slug
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id", None)
        slug = request.GET.get("slug", None)
        if id is not None:
            try:
                medical_association = MedicalAssociation.objects.get(
                    id=id, is_approved=True
                )
            except MedicalAssociation.DoesNotExist:
                medical_association = None
        elif slug is not None:
            try:
                medical_association = MedicalAssociation.objects.get(
                    slug=slug, is_approved=True
                )
            except MedicalAssociation.DoesNotExist:
                medical_association = None
        else:
            medical_association = None

        if medical_association is not None:
            serializer = MedicalAssociationPublicSerializer(medical_association)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


################################################################################
# Doctor Association
################################################################################


class ApiPublicDoctorAssociationList(APIView):
    """
    Get Medical Associations of doctor profile
    ?user=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, id=request.GET.get("user", None))
        if user.doctor_profile():
            associations = user.doctor_profile().get_associations_rel()
            serializer = DoctorAssociationSerializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                "User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND
            )


class ApiPrivateDoctorAssociationCreate(APIView):
    """
    Create Medical Association to doctor profile
    ?user=n
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.doctor_profile():
            serializer = DoctorAssociationCreateSerializer(data=request.data)

            if serializer.is_valid():
                doctor_association_kwargs = serializer.validated_data
                doctor_association_kwargs["doctor"] = user.doctor_profile()

                doctor_association = DoctorAssociation(**doctor_association_kwargs)
                try:
                    doctor_association.save()
                except IntegrityError:
                    return Response(
                        {
                            "Duplicate Medical Association": "You are already a member of this association!"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ValueError as err:
                    return Response(
                        {"Value Error": str(err)}, status=status.HTTP_400_BAD_REQUEST
                    )
                return_serializer = DoctorAssociationSerializer(doctor_association)
                return Response(return_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND
            )


class ApiPrivateDoctorAssociationUpdate(APIView):
    """
    Updates Medical Association of doctor profile
    ?association=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_association = get_object_or_404(
            DoctorAssociation,
            id=request.GET.get("association", None),
            doctor=request.user.doctorprofile,
        )

        serializer = DoctorAssociationUpdateSerializer(data=request.data)

        if serializer.is_valid():
            doctor_association.level = serializer.validated_data["level"]
            doctor_association.year_attained = serializer.validated_data[
                "year_attained"
            ]
            doctor_association.save()
            return_serializer = DoctorAssociationSerializer(doctor_association)
            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ApiPrivateDoctorAssociationDelete(APIView):
    """
    Deletes Medical Association of doctor profile
    ?association=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_association = get_object_or_404(
            DoctorAssociation,
            id=request.GET.get("association", None),
            doctor=request.user.doctorprofile,
        )

        doctor_association.delete()
        return Response("Association deleted", status=status.HTTP_200_OK)


class ApiPrivateDoctorAssociationDetail(APIView):
    """
    Detail of Medical Association of doctor profile
    ?association=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_association = get_object_or_404(
            DoctorAssociation,
            id=request.GET.get("association", None),
            doctor=request.user.doctorprofile,
        )

        serializer = DoctorAssociationSerializer(doctor_association)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicDoctorAssociationDetail(APIView):
    """
    Public details of Medical Association
    ?association=id
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor_association = get_object_or_404(
            DoctorAssociation, id=request.GET.get("association", None)
        )

        serializer = DoctorAssociationPublicSerializer(doctor_association)
        return Response(serializer.data, status=status.HTTP_200_OK)
