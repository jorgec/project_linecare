from django.urls import reverse
from rest_framework import serializers

from datesdim.serializers import DateDimSerializer, TimeDimSerializer
from doctor_profiles.constants import QUEUE_INACTIVE, QUEUE_ACTIVE
from doctor_profiles.models import PatientAppointment
from doctor_profiles.serializers import MedicalInstitutionSerializer
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
    medical_institution = MedicalInstitutionSerializer()
    last_visit = serializers.SerializerMethodField('repr_last_visit')

    def repr_prior_visits(self, obj):
        return PatientAppointment.objects.prior_visits(
            doctor=obj.doctor,
            patient=obj.patient
        ).count()

    def repr_last_visit(self, obj):
        visit = PatientAppointment.objects.filter(
            doctor=obj.doctor,
            patient=obj.patient,
            schedule_day__date_obj__lte=obj.schedule_day.date_obj,
        ).exclude(
            id=obj.id
        ).first()

        if visit:
            return {
                'date': f'{visit.schedule_day}',
                'id': visit.id,
                'url': f"{reverse('doctor_profile_patient_appointment_detail')}?appointment={visit.id}"
            }
        return {
            'date': None,
            'id': None,
            'url': ''
        }

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
            'status_display',
            'last_visit'
        )
