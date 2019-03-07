from django.urls import reverse
from rest_framework import serializers

from datesdim.serializers import DateDimSerializer, TimeDimSerializer
from doctor_profiles.constants import QUEUE_INACTIVE, QUEUE_ACTIVE, QUEUE_NOT_CANCELLED_CODES
from doctor_profiles.models import PatientAppointment
from doctor_profiles.serializers import MedicalInstitutionSerializer
from profiles.serializers import BaseProfilePrivateSerializerFull
from biometrics.serializers import BiometricSerializer
from biometrics.models import Biometric

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


class PatientAppointmentHistoryListSerializer(serializers.ModelSerializer):
    schedule_day = DateDimSerializer()
    time_start = TimeDimSerializer()
    time_end = TimeDimSerializer()
    queue_status = serializers.SerializerMethodField('repr_queue_status')
    status_display = serializers.SerializerMethodField('repr_status_display')
    type = serializers.SerializerMethodField('repr_type')
    medical_institution = MedicalInstitutionSerializer()
    appointment_url = serializers.SerializerMethodField('repr_appointment_url')

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

    def repr_appointment_url(self, obj):
        return f"{reverse('doctor_profile_patient_appointment_detail')}?appointment={obj.id}"

    class Meta:
        model = PatientAppointment
        fields = (
            'id',
            'schedule_day',
            'time_start',
            'time_end',
            'queue_status',
            'status_display',
            'type',
            'medical_institution',
            'appointment_url'
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
    patient_url = serializers.SerializerMethodField('repr_patient_url')
    schedule = serializers.SerializerMethodField('repr_schedule')
    biometrics = serializers.SerializerMethodField('repr_biometrics')

    def repr_biometrics(self, obj):
        try:
            biometrics = Biometric.objects.get(profile=obj.patient)
            serializer = BiometricSerializer(biometrics)
            return serializer.data
        except Biometric.DoesNotExist:
            return None

    def repr_schedule(self, obj):
        if obj.schedule_day_object:
            return obj.schedule_day_object.schedule.id
        return None

    def repr_prior_visits(self, obj):
        return PatientAppointment.objects.prior_visits(
            doctor=obj.doctor,
            patient=obj.patient
        ).count()

    def repr_patient_url(self, obj):
        return reverse('doctor_profile_patient_detail', kwargs={
            'patient_id': obj.patient.id
        })

    def repr_last_visit(self, obj):
        visit = PatientAppointment.objects.filter(
            doctor=obj.doctor,
            patient=obj.patient,
            schedule_day__date_obj__lte=obj.schedule_day.date_obj,
            status__in=QUEUE_NOT_CANCELLED_CODES
        ).exclude(
            id=obj.id
        ).order_by('-schedule_day__date_obj').first()

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
            'last_visit',
            'patient_url',
            'schedule',
            'biometrics'
        )
