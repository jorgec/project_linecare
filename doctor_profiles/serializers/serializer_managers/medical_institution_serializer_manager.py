from rest_framework.utils import json

from doctor_profiles.serializers.medical_institution_serializers import MedicalInstitutionLocationPublicSerializer, \
    MedicalInstitutionLocationSerializer, MedicalInstitutionSerializer, MedicalInstitutionPublicSerializer, \
    MedicalInstitutionNestedPublicSerializer, MedicalInstitutionLocationPublicSerializerWithVotes, \
    MedicalInstitutionPhonesPublicSerializerWithVotes, MedicalInstitutionCoordinatePublicSerializerWithVotes


class MedicalInstitutionLocationSerializerManager:
    public_serializer = MedicalInstitutionLocationPublicSerializer
    private_serializer = MedicalInstitutionLocationSerializer

    def serialize(self, instance, *, public=True, many=False):
        if public:
            return self.public_serializer(instance, many=many)
        return self.private_serializer(instance, many=many)


class MedicalInstitutionSerializerManager:
    public_serializer = MedicalInstitutionPublicSerializer
    private_serializer = MedicalInstitutionSerializer

    public_nested_serializer = MedicalInstitutionNestedPublicSerializer

    def serialize(self, instance, *, public=True, many=False):
        if public:
            return self.public_serializer(instance, many=many)
        return self.private_serializer(instance, many=many)

    def serialize_nested(self, instance, *, public=True):
        institution = self.public_serializer(instance)
        address = MedicalInstitutionLocationPublicSerializerWithVotes(instance.addresses(), many=True)
        phones = MedicalInstitutionPhonesPublicSerializerWithVotes(instance.phones(), many=True)
        coordinates = MedicalInstitutionCoordinatePublicSerializerWithVotes(instance.all_coordinates(), many=True)

        nested = {
            'institution': institution.data,
            'address': address.data,
            'phones': phones.data,
            'coordinates': coordinates.data
        }

        # return json.dumps(nested)
        return nested
