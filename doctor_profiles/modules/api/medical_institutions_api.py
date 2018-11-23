from django.db import IntegrityError
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import MedicalInstitution, MedicalInstitutionLocation, MedicalInstitutionLocationVote
from doctor_profiles.serializers.medical_institution_serializers import MedicalInstitutionPublicSerializer, \
    MedicalInstitutionLocationPublicSerializer, MedicalInstitutionPhonePublicSerializer, \
    MedicalInstitutionLocationCreateSerializer
from doctor_profiles.serializers.serializer_managers.medical_institution_serializer_manager import \
    MedicalInstitutionSerializerManager


class ApiPublicMedicalInstitutionSearch(APIView):
    def get(self, request, *args, **kwargs):
        pass


class ApiPublicMedicalInstitutionList(APIView):
    """
    List all approved medical institutions
    """
    model = MedicalInstitution
    serializer_class = MedicalInstitutionPublicSerializer

    def get(self, request, *args, **kwargs):
        filters = {
            'is_approved': True
        }

        region = request.GET.get('region', None)
        province = request.GET.get('province', None)
        city = request.GET.get('city', None)

        obj = self.model.objects.filter(**filters)

        if region:
            obj = obj.by_region(region=region)

        if province:
            obj = obj.by_province(province=province)

        if city:
            obj = obj.by_city(city=city)

        serializer = self.serializer_class(obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionDetail(APIView):
    """
    Detail of requested medical institution
    id=n or slug=s
    """
    model = MedicalInstitution

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        slug = request.GET.get('slug', None)
        if id is not None:
            try:
                obj = self.model.objects.get(id=id, is_approved=True)
            except self.model.DoesNotExist:
                obj = None
        elif slug is not None:
            try:
                obj = self.model.objects.get(slug=slug, is_approved=True)
            except self.model.DoesNotExist:
                obj = None
        else:
            obj = None

        if obj is not None:
            serializer_manager = MedicalInstitutionSerializerManager()
            return Response(serializer_manager.serialize_nested(obj), status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ApiPrivateMedicalInstitutionLocationVoteUp(APIView):
    """
    Vote up a location for a medical institution
    location=id
    """
    permission_classes = [permissions.IsAuthenticated]
    model = MedicalInstitutionLocation

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        loc = get_object_or_404(MedicalInstitutionLocation, id=id)

        try:
            loc.vote_up(user=request.user)
            return Response("Thanks for voting", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("You've already voted for this location", status=status.HTTP_409_CONFLICT)


class ApiPrivateMedicalInstitutionLocationVoteDown(APIView):
    """
    Vote down a location for a medical institution
    location=id
    """
    permission_classes = [permissions.IsAuthenticated]
    model = MedicalInstitutionLocation

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        loc = get_object_or_404(MedicalInstitutionLocation, id=id)

        try:
            loc.vote_down(user=request.user)
            return Response("Thanks for voting", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("You've already voted for this location", status=status.HTTP_409_CONFLICT)


class ApiPrivateMedicalInstitutionLocationCreate(APIView):
    """
    Add/suggest a new location for medical institution
    ?id=n

    POST KWARGS:
    :param country (optional):
    :type int:
    :param region:
    :type int:
    :param province:
    :type int:
    :param city:
    :type int:
    :param address:
    :type str:
    :param lat:
    :type decimal/float:
    :param lon:
    :type decimal/float:

    """

    permission_classes = [permissions.IsAuthenticated]
    model = MedicalInstitutionLocation

    def post(self, request, *args, **kwargs):
        """
        POST KWARGS:
        :param country (optional):
        :type int:
        :param region:
        :type int:
        :param province:
        :type int:
        :param city:
        :type int:
        :param address:
        :type str:
        :param lat:
        :type decimal/float:
        :param lon:
        :type decimal/float:
        :return:
        :rtype:
        """
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id'))

        serializer = MedicalInstitutionLocationCreateSerializer(data=request.data)
        if serializer.is_valid():
            locdata = serializer.validated_data
            locdata['suggested_by'] = request.user
            locdata['medical_institution'] = medical_institution

            location = MedicalInstitutionLocation.objects.create(**locdata)

            return_serializer = MedicalInstitutionLocationPublicSerializer(location)

            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
