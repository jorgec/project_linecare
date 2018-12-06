from rest_framework import serializers

from datesdim.serializers import TimeDimSerializer, DateDimSerializer
from doctor_profiles.models import DoctorSchedule
from doctor_profiles.serializers import DoctorProfileSerializer, MedicalInstitutionSerializer


class DoctorScheduleCreateRegularScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = (
            'days',
            'medical_institution',
        )


class DoctorScheduleSerializer(serializers.ModelSerializer):
    start_time = TimeDimSerializer()
    end_time = TimeDimSerializer()
    start_date = DateDimSerializer()
    end_date = DateDimSerializer()
    doctor = DoctorProfileSerializer()
    medical_institution = MedicalInstitutionSerializer()

    class Meta:
        model = DoctorSchedule
        fields = '__all__'
