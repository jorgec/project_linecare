from rest_framework import serializers

from datesdim.serializers import DateDimSerializer, TimeDimSerializer
from doctor_profiles.constants import QUEUE_INACTIVE, QUEUE_ACTIVE
from doctor_profiles.models import PatientAppointment
from profiles.serializers import BaseProfilePrivateSerializerFull

class PatientAppointmentSerializer(serializers.ModelSerializer):
    patient = BaseProfilePrivateSerializerFull()
    schedule_day = DateDimSerializer()
    time_start = TimeDimSerializer()
    time_end = TimeDimSerializer()
    type = serializers.SerializerMethodField('repr_type')

    def repr_type(self, obj):
        return obj.get_type_display()

    class Meta:
        model = PatientAppointment
        fields = (
            'id',
            'schedule_day',
            'time_start',
            'time_end',
            'patient',
            'doctor',
            'medical_institution',
            'schedule_day_object',
            'type',
        )


class PatientQueuePrivateSerializer(serializers.ModelSerializer):
    patient = BaseProfilePrivateSerializerFull()
    schedule_day = DateDimSerializer()
    time_start = TimeDimSerializer()
    time_end = TimeDimSerializer()
    prior_visits = serializers.SerializerMethodField('repr_prior_visits')
    queue_status = serializers.SerializerMethodField('repr_queue_status')
    status_display = serializers.SerializerMethodField('repr_status_display')
    type = serializers.SerializerMethodField('repr_type')

    def repr_prior_visits(self, obj):
        return PatientAppointment.objects.prior_visits(
            doctor=obj.doctor,
            patient=obj.patient
        ).count()

    def repr_queue_status(self, obj):
        if obj.status in QUEUE_INACTIVE:
            return 'inactive'
        elif obj.status in QUEUE_ACTIVE:
            return 'active'
        else:
            return 'waiting'

    def repr_type(self, obj):
        return obj.get_type_display()

    def repr_status_display(self, obj):
        return obj.get_status_display()

    class Meta:
        model = PatientAppointment
        fields = (
            'id',
            'metadata',
            'status',
            'schedule_day',
            'time_start',
            'time_end',
            'patient',
            'doctor',
            'medical_institution',
            'schedule_day_object',
            'prior_visits',
            'type',
            'queue_status',
            'queue_number',
            'status_display'
        )
