from django.db import IntegrityError
from rest_framework import status, permissions, parsers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import MedicalInstitution, MedicalInstitutionLocation, MedicalInstitutionType, DoctorProfile
from doctor_profiles.models.medical_institution_location_models import MedicalInstitutionCoordinate
from doctor_profiles.serializers import MedicalInstitutionTypePublicSerializer, MedicalInstitutionPublicSerializer, \
    MedicalInstitutionCreatePrivateSerializer, MedicalInstitutionLocationPublicSerializerWithVotes, \
    MedicalInstitutionLocationCreateSerializer, MedicalInstitutionLocationPublicSerializer, \
    MedicalInstitutionCoordinatePublicSerializerWithVotes, MedicalInstitutionCoordinatesCreateSerializer
from doctor_profiles.serializers.serializer_managers.medical_institution_serializer_manager import \
    MedicalInstitutionSerializerManager
from profiles.modules.response_templates.profile import private_profile_template
from receptionist_profiles.modules.response_templates.receptionist_profile import private_receptionist_profile_template
from receptionist_profiles.serializers.receptionist_profile_serializers import ReceptionistProfileSerializer


class ApiPublicMedicalInstitutionSearch(APIView):
    def get(self, request, *args, **kwargs):
        pass


class ApiPublicMedicalInstitutionTypeList(APIView):
    """
    List all medical institution types
    """

    def get(self, request, *args, **kwargs):
        types = MedicalInstitutionType.objects.filter(is_approved=True)
        serializer = MedicalInstitutionTypePublicSerializer(types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        s = request.GET.get('s', None)

        obj = self.model.objects.filter(**filters)

        if region:
            obj = obj.by_region(region=region)

        if province:
            obj = obj.by_province(province=province)

        if city:
            obj = obj.by_city(city=city)

        if s:
            obj = obj.by_name(s=s)

        serializer = self.serializer_class(obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionDetail(APIView):
    """
    Detail of requested medical institution
    id=n or slug=s
    """
    model = MedicalInstitution
    permission_classes = [permissions.AllowAny]

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


class ApiPrivateMedicalInstitutionCreate(APIView):
    """
    Create new medical institution
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = MedicalInstitutionCreatePrivateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                mi = MedicalInstitution.objects.create(
                    name=serializer.validated_data['name'],
                    type_id=serializer.validated_data['type'],
                    added_by=request.user
                )
            except IntegrityError:
                return Response("Duplicate name", status=status.HTTP_400_BAD_REQUEST)

            try:
                loc = MedicalInstitutionLocation.objects.create(
                    address=serializer.validated_data['address'],
                    region_id=serializer.validated_data['region'],
                    province_id=serializer.validated_data['province'],
                    city_id=serializer.validated_data['city'],
                    zip_code=serializer.validated_data['zip_code'],
                    suggested_by=request.user,
                    medical_institution=mi
                )

            except IntegrityError:
                return Response("Duplicate address", status=status.HTTP_400_BAD_REQUEST)

            return_serializer = MedicalInstitutionPublicSerializer(mi)

            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicMedicalInstitutionAddressList(APIView):
    """
    List of medical instituion addresses
    ?id=medical_institution_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))
        serializer = MedicalInstitutionLocationPublicSerializerWithVotes(medical_institution.addresses(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionTopAddressDetail(APIView):
    """
    Detail of top medical instituion addresses
    ?id=medical_institution_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))
        serializer = MedicalInstitutionLocationPublicSerializerWithVotes(medical_institution.address())

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionAddressDetail(APIView):
    """
    Detail of medical instituion addresses
    ?id=medical_institution_location_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        location = get_object_or_404(MedicalInstitutionLocation, id=request.GET.get('id', None))
        serializer = MedicalInstitutionLocationPublicSerializerWithVotes(location.get_address_with_votes())

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateMedicalInstitutionLocationVoteUp(APIView):
    """
    Vote up a location for a medical institution
    ?location=id
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
            return Response("You've already upvoted this location", status=status.HTTP_409_CONFLICT)


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
    ?id=medical_institution_id

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
        :param zip_code:
        :type positive small int:
        :param address:
        :type str:
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


###############################################################################
# Coordinates
###############################################################################
class ApiPublicMedicalInstitutionCoordinateList(APIView):
    """
    List of coordinates for medical institution
    ?id=medical_institution_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))
        serializer = MedicalInstitutionCoordinatePublicSerializerWithVotes(medical_institution.all_coordinates(),
                                                                           many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionTopCoordinateDetail(APIView):
    """
    Detail of top coords for medical institution
    ?id=medical_institution_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))
        serializer = MedicalInstitutionCoordinatePublicSerializerWithVotes(medical_institution.coordinates())

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicMedicalInstitutionCoordinateDetail(APIView):
    """
        Detail of oords
        ?id=coords_id
        """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        coords = get_object_or_404(MedicalInstitutionCoordinate, id=request.GET.get('id', None))
        serializer = MedicalInstitutionCoordinatePublicSerializerWithVotes(coords)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateMedicalInstitutionCoordinateVoteDown(APIView):
    """
    Vote up coordinates
    ?coordinate=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        coords = get_object_or_404(MedicalInstitutionCoordinate, id=id)

        try:
            coords.vote_down(user=request.user)
            return Response("Thanks for voting", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("You've already downvoted this coordinate", status=status.HTTP_409_CONFLICT)


class ApiPrivateMedicalInstitutionCoordinateVoteUp(APIView):
    """
    Vote up coordinates
    ?coordinate=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        coords = get_object_or_404(MedicalInstitutionCoordinate, id=id)

        try:
            coords.vote_up(user=request.user)
            return Response("Thanks for voting", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("You've already upvoted this coordinate", status=status.HTTP_409_CONFLICT)


class ApiPrivateMedicalInstitutionCoordinateCreate(APIView):
    """
    Add/suggest a new coordinate pair for medical institution
    ?id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id'))
        serializer = MedicalInstitutionCoordinatesCreateSerializer(data=request.data)
        if serializer.is_valid():
            locdata = serializer.validated_data
            locdata['medical_institution'] = medical_institution
            locdata['suggested_by'] = request.user

            coords = MedicalInstitutionCoordinate.objects.create(**locdata)

            return Response("Coordinates saved", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############################################################################
# Receptionists
###############################################################################

class ApiPrivateMedicalInstitutionReceptionistList(APIView):
    """
    List of receptionists in this medical institution
    ?id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id'))
        rel = medical_institution.institution_connections.filter(is_approved=True)
        receptionists = [r.receptionist for r in rel]
        serializer = ReceptionistProfileSerializer(receptionists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateMedicalInstitutionNotConnectedReceptionistList(APIView):
    """
    List of receptionists in this medical institution not connected to doctor
    ?id=medical_institution_id&doctor_id=doctor_id
    [optional]
    ?fmt=[full] - returns serialized private profile objects
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id'))
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))
        rel = medical_institution.institution_connections.filter(is_approved=True).exclude(doctor=doctor)
        receptionists = [r.receptionist for r in rel]

        if request.GET.get('fmt', None) == 'full':
            serializer_list = []
            for r in receptionists:
                serializer_list.append(private_receptionist_profile_template(user=r.user))

            return Response(serializer_list, status=status.HTTP_200_OK)
        else:
            serializer = ReceptionistProfileSerializer(receptionists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateMedicalInstitutionConnectedReceptionistList(APIView):
    """
    List of receptionists in this medical institution of doctor
    ?id=medical_institution_id&doctor_id=doctor_id
    [optional]
    ?fmt=[full] - returns serialized private profile objects
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id'))
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))
        receptionists = doctor.get_receptionists(medical_institution=medical_institution)

        if request.GET.get('fmt', None) == 'full':
            serializer_list = []
            for r in receptionists:
                serializer_list.append(private_receptionist_profile_template(user=r.user))

            return Response(serializer_list, status=status.HTTP_200_OK)
        else:
            serializer = ReceptionistProfileSerializer(receptionists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
