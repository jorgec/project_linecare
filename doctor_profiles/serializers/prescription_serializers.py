from rest_framework import serializers

from doctor_profiles.models.patient_checkup_models import Prescription
from drug_information.serializers.drug_serializers import DrugSerializer, DrugRouteSerializer


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            'drug',
            'checkup',
            'doctor',
            'prescription_dosage',
            'prescription_dosage_unit',
            'prescription_amount',
            'prescription_amount_unit',
            'prescription_route',
            'prescription_frequency',
            'prescription_dispense_qty',
            'prescription_notes',
        )


class PatientPrescriptionSerializer(serializers.ModelSerializer):
    drug = DrugSerializer()
    prescription_route = DrugRouteSerializer()
    class Meta:
        model = Prescription
        fields = (
            'id',
            'drug',
            'checkup',
            'doctor',
            'prescription_dosage',
            'prescription_dosage_unit',
            'prescription_amount',
            'prescription_amount_unit',
            'prescription_route',
            'prescription_frequency',
            'prescription_dispense_qty',
            'prescription_notes',
        )