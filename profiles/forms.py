from django import forms

from profiles.models import BaseProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BaseProfile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender'
        )
        labels = {
            'gender': 'Sex'
        }
