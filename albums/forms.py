from django import forms

from albums.models import Photo


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = (
            'photo',
            'caption',
            'is_public',
        )
