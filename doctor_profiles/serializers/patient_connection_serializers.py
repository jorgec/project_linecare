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
    patient_detail_url = serializers.SerializerMethodField('repr_patient_url')
    prior_visits = serializers.SerializerMethodField('repr_prior_visits')

    def repr_patient_url(self, obj):
        url = reverse('doctor_profile_patient_detail', kwargs={
            'patient_id': obj.id
        })
        return url

    def repr_prior_visits(self, obj):
        return PatientAppointment.objects.prior_visits(
            doctor=obj.doctor,
            patient=obj.patient
        ).count()


    class Meta:
        model = PatientConnection
        fields = (
            'id',
            'created',
            'doctor',
            'patient',
            'patient_detail_url',
            'prior_visits'
        )