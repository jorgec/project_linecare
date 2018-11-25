from django import forms

from doctor_profiles.models import MedicalInstitutionLocation
from .models import Specialization, InsuranceProvider, DoctorProfile, MedicalDegree, MedicalAssociation, \
    DoctorSpecialization, DoctorInsurance, DoctorDegree, DoctorAssociation


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name', 'metadata', 'abbreviation', 'parent']


class InsuranceProviderForm(forms.ModelForm):
    class Meta:
        model = InsuranceProvider
        fields = ['name', 'metadata']


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['metadata']


class MedicalDegreeForm(forms.ModelForm):
    class Meta:
        model = MedicalDegree
        fields = ['name', 'abbreviation']


class MedicalAssociationForm(forms.ModelForm):
    class Meta:
        model = MedicalAssociation
        fields = ['name', 'abbreviation', 'metadata']


class DoctorSpecializationForm(forms.ModelForm):
    class Meta:
        model = DoctorSpecialization
        fields = ['year_attained', 'place_of_residency', 'doctor', 'specialization']


class DoctorInsuranceForm(forms.ModelForm):
    class Meta:
        model = DoctorInsurance
        fields = ['identifier', 'doctor', 'insurance']


class DoctorDegreeForm(forms.ModelForm):
    class Meta:
        model = DoctorDegree
        fields = ['year_attained', 'school', 'license_number', 'doctor', 'degree']


class DoctorDegreeEditForm(forms.ModelForm):
    class Meta:
        model = DoctorDegree
        fields = ['year_attained', 'school', 'license_number']


class DoctorDegreeCreateForm(forms.ModelForm):
    class Meta:
        model = DoctorDegree
        fields = ['year_attained', 'school', 'metadata', 'license_number', 'degree']


class DoctorAssociationForm(forms.ModelForm):
    class Meta:
        model = DoctorAssociation
        fields = ['level', 'year_attained', 'doctor', 'association']


class MedicalInstitutionLocationForm(forms.ModelForm):
    class Meta:
        model = MedicalInstitutionLocation
        fields = ['address', 'region', 'province', 'city', 'zip_code']
