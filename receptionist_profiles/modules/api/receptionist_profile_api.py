from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import DoctorProfile, MedicalInstitution
from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.models.receptionist_profile_model import ReceptionistConnection
from receptionist_profiles.serializers import ReceptionistProfileCreateByDoctorSerializer, \
    ReceptionistProfileSerializer, ReceptionistConnectionPrivateBasicSerializer


class ApiPrivateReceptionistConnectionCreate(APIView):
    """
    Create a connection between a receptionist profile and either a doctor or medical institution
    ?receptionist_id=receptionist_id
    [one optional]
    ?doctor_id=doctor_id
    -or-
    ?medical_institution_id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receptionist_profile = get_object_or_404(ReceptionistProfile, id=request.POST.get('receptionist_id', None))

        params = {
            'receptionist': receptionist_profile
        }

        doctor_id = request.POST.get('doctor_id', None)
        medical_institution_id = request.POST.get('medical_institution_id', None)

        if doctor_id:
            doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
            params['doctor'] = doctor_profile

        if medical_institution_id:
            medical_institution = get_object_or_404(MedicalInstitution, id=medical_institution_id)
            params['medical_institution'] = medical_institution

        try:
            connection = ReceptionistConnection.objects.create(
                **params
            )
            serializer = ReceptionistConnectionPrivateBasicSerializer(connection)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response("This connection already exists!", status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(f"{e}\n doctor: {doctor_id}, receptionist: {receptionist_profile}, mi: {medical_institution_id}")


class ApiPrivateReceptionistConnectionDelete(APIView):
    """
    Removes a connection
    ?receptionist_id=receptionist_id&doctor_id=doctor_id&medical_institution_id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receptionist_profile = get_object_or_404(ReceptionistProfile, id=request.POST.get('receptionist_id', None))

        params = {
            'receptionist': receptionist_profile
        }

        doctor_id = request.POST.get('doctor_id', None)
        medical_institution_id = request.POST.get('medical_institution_id', None)

        if doctor_id:
            doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
            params['doctor'] = doctor_profile

        if medical_institution_id:
            medical_institution = get_object_or_404(MedicalInstitution, id=medical_institution_id)
            params['medical_institution'] = medical_institution

        try:
            connection = ReceptionistConnection.objects.get(
                **params
            )

            connection.delete()
            return Response("Connection removed", status=status.HTTP_200_OK)

        except ReceptionistConnection.DoesNotExist:
            return Response("This connection does not exist!", status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateReceptionistProfileCreateByDoctor(APIView):
    """
    Create a receptionist profile for someone via a doctor account
    ?doctor_id=doctor_id&medical_institution_id=medical_institution_id

    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution_id', None))

        serializer = ReceptionistProfileCreateByDoctorSerializer(data=request.data)

        if serializer.is_valid():

            try:
                account = Account.objects.create_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
            except IntegrityError:
                return Response("That email is already registered!", status=status.HTTP_409_CONFLICT)

            profile = account.base_profile()
            profile.first_name = serializer.validated_data['first_name']
            profile.last_name = serializer.validated_data['last_name']
            profile.is_fresh = False
            profile.save()

            ReceptionistProfile.objects.create_by_doctor(
                doctor=None,
                medical_institution=medical_institution,
                user=account
            )

            receptionist = ReceptionistProfile.objects.create_by_doctor(
                doctor=doctor,
                medical_institution=medical_institution,
                user=account
            )

            return_serializer = ReceptionistProfileSerializer(receptionist)

            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
