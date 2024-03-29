import re
from django.db import models

# Create your models here.
from django.db.models import Model

from biometrics.constants import BLOOD_TYPE_CHOICES
from biometrics.managers import BiometricManager


class Biometric(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # metrics
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    blood_type = models.CharField(choices=BLOOD_TYPE_CHOICES, max_length=3, null=True, blank=True)

    # Relationship Fields
    profile = models.OneToOneField('profiles.BaseProfile', related_name='profile_biometrics', on_delete=models.SET_NULL,
                                null=True, blank=True)

    objects = BiometricManager()

    class Meta:
        ordering = ('profile',)

    def __str__(self):
        return f"{self.profile} biometrics"

    def as_html(self):
        html_display = {
            'Height': f"{round(self.height)} cm ({self.height_to_us()})",
            'Weight': f"{round(self.weight)} kg ({self.weight_to_us()})",
            'Blood Type': self.blood_type,
        }
        html = ''
        for key, value in html_display.items():
            html = f"{html}<p class='kv-pair kv-pair-center'><span class='kv-key'>{key}</span><span class='kv-value'>{value}</p>"
        return html

    def height_to_us(self):
        feet, inches = divmod(self.height * 0.393701, 12)
        return f"{int(feet)}'{int(inches)}\""

    def weight_to_us(self):
        lb = self.weight * 2.2
        return f"{round(lb)} lbs"
