from rest_framework import serializers

from doctor_profiles.models import MedicalInstitutionType, MedicalInstitutionLocation, MedicalInstitutionLocationVote, \
    MedicalInstitutionPhone, MedicalInstitutionPhoneVote, MedicalInstitution
from locations.serializers import RegionSerializer, CountrySerializer, ProvinceSerializer, CitySerializer


class MedicalInstitutionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionType
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'metadata',
        )


class MedicalInstitutionTypePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionType
        fields = (
            'id',
            'slug',
            'name',
        )


class MedicalInstitutionLocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    region = RegionSerializer()
    province = ProvinceSerializer()
    city = CitySerializer()

    class Meta:
        model = MedicalInstitutionLocation
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'is_approved',
            'lat',
            'lon',
            'country',
            'region',
            'province',
            'city',
            'address',
        )



class MedicalInstitutionLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionLocation
        fields = (
            'lat',
            'lon',
            'country',
            'region',
            'province',
            'city',
            'address',
        )


class MedicalInstitutionLocationPublicSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    region = RegionSerializer()
    province = ProvinceSerializer()
    city = CitySerializer()

    class Meta:
        model = MedicalInstitutionLocation
        fields = (
            'id',
            'lat',
            'lon',
            'country',
            'region',
            'province',
            'city',
            'address',
        )


class MedicalInstitutionLocationVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionLocationVote
        fields = (
            'id',
            'created',
            'last_updated',
            'type',
        )


class MedicalInstitutionPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionPhone
        fields = (
            'id',
            'created',
            'last_updated',
            'phone_number',
        )


class MedicalInstitutionPhonePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionPhone
        fields = (
            'id',
            'phone_number',
        )


class MedicalInstitutionPhoneVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionPhoneVote
        fields = (
            'id',
            'created',
            'last_updated',
            'type',
        )


class MedicalInstitutionSerializer(serializers.ModelSerializer):
    type = MedicalInstitutionTypeSerializer()

    class Meta:
        model = MedicalInstitution
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'is_approved',
            'metadata',
            'type'
        )


class MedicalInstitutionPublicSerializer(serializers.ModelSerializer):
    type = MedicalInstitutionTypePublicSerializer()

    class Meta:
        model = MedicalInstitution
        fields = (
            'id',
            'slug',
            'name',
            'type'
        )


class MedicalInstitutionLocationPublicSerializerWithVotes(serializers.Serializer):
    address = MedicalInstitutionLocationPublicSerializer()
    votes = serializers.IntegerField()


class MedicalInstitutionPhonesPublicSerializerWithVotes(serializers.Serializer):
    phone = MedicalInstitutionPhonePublicSerializer()
    votes = serializers.IntegerField()


class MedicalInstitutionNestedPublicSerializer(serializers.Serializer):
    institution = MedicalInstitutionPublicSerializer()
    address = MedicalInstitutionLocationPublicSerializerWithVotes(allow_null=True, required=False, many=True)
    phones = MedicalInstitutionPhonesPublicSerializerWithVotes(allow_null=True, required=False, many=True)
