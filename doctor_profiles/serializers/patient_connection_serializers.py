from django.urls import reverse
from rest_framework import serializers

from doctor_profiles.models import PatientConnection, PatientAppointment
from doctor_profiles.serializers import DoctorProfileSerializer
from profiles.serializers import ProfileSerializer, BaseProfilePrivateSerializerFull


class PatientConnectionSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    patient = ProfileSerializer()

    class Meta:
        model = PatientConnection
        fields = (
            'id',
            'created',
            'doctor',
            'patient'
        )


class PatientConnectionDoctorViewSerializer(serializers.ModelSerializer):
    patient = BaseProfilePrivateSerializerFull()
    prior_visits = serializers.SerializerMethodField('repr_prior_visits')
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

    class Meta:
        model = PatientConnection
        fields = (
            'id',
            'created',
            'doctor',
            'patient',
            'prior_visits',
            'last_visit'
        )
