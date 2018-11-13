from django import forms

from biometrics.models import Biometric


class BiometricForm(forms.ModelForm):
    class Meta:
        model = Biometric
        fields = (
            'height',
            'weight',
            'blood_type',
        )
        widgets = {
            'height': forms.TextInput,
            'weight': forms.TextInput
        }
        help_texts = {
            'weight': 'Enter the value either in kilograms (ex: 50kg or just 50) or pounds (ex: 50lb or 50lbs) &mdash; the value will be converted to kilograms.',
            'height': 'Enter the value in centimeters (ex: 180cm or just 180) or in feet and inches (ex: 5\' 7") &mdash; the value will be converted to centimeters.'
        }