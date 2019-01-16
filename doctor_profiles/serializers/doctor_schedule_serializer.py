from rest_framework import serializers

from datesdim.serializers import TimeDimSerializer, DateDimSerializer
from doctor_profiles.models import DoctorSchedule, DoctorScheduleDay
from doctor_profiles.serializers import DoctorProfileSerializer, MedicalInstitutionSerializer, \
    MedicalInstitutionPublicSerializer


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
    medical_institution = MedicalInstitutionPublicSerializer()
    days_split = serializers.SerializerMethodField('repr_days_split')

    def repr_days_split(self, obj):
        return obj.split_days()

    class Meta:
        model = DoctorSchedule
        fields = (
            'id',
            'start_time',
            'end_time',
            'start_date',
            'end_date',
            'doctor',
            'medical_institution',
            'days',
            'days_split'
        )


class DoctorScheduleBasicSerializer(serializers.ModelSerializer):
    start_time = TimeDimSerializer()
    end_time = TimeDimSerializer()
    start_date = DateDimSerializer()
    end_date = DateDimSerializer()
    days_split = serializers.SerializerMethodField('repr_days_split')

    def repr_days_split(self, obj):
        return obj.split_days()

    class Meta:
        model = DoctorSchedule
        fields = (
            'id',
            'start_time',
            'end_time',
            'start_date',
            'end_date',
            'days',
            'days_split',
            'medical_institution'
        )



class DoctorScheduleCollisionSerializer(serializers.Serializer):
    medical_institution = MedicalInstitutionSerializer()
    day = DateDimSerializer()
    schedule = DoctorScheduleSerializer()
    start_time = TimeDimSerializer()
    end_time = TimeDimSerializer()


class DoctorScheduleDaySerializer(serializers.ModelSerializer):
    schedule = DoctorScheduleBasicSerializer()
    medical_institution = MedicalInstitutionPublicSerializer()
    class Meta:
        model = DoctorScheduleDay
        fields = (
            'id',
            'day',
            'doctor',
            'medical_institution',
            'schedule',
            'doctor_id_in',
            'doctor_stepped_out',
            'actual_start_time',
            'actual_end_time'
        )

