import re
from django.db import models


class BiometricQuerySet(models.QuerySet):
    def none(self):
        return self


class BiometricManager(models.Manager):
    height_pattern = re.compile(r"([0-9]+)'\s?([0-9]*\.?[0-9]+)\"")
    non_decimal = re.compile(r'[^\d.]+')

    def get_queryset(self):
        return BiometricQuerySet(self.model, using=self._db)

    def validate(self, *args, **kwargs):
        height, weight = None, None
        if 'height' in kwargs:
            __height = kwargs['height']
            height_match = self.height_pattern.match(__height)
            if height_match is None:
                try:
                    height = float(__height)
                except ValueError:
                    return False, f"Bad Height: {__height}"
            else:
                feet, inches = list(map(lambda x: float(x), height_match.groups()))
                height = (inches + (feet * 12)) * 2.54

        if 'weight' in kwargs:
            __weight = kwargs['weight'].lower()
            __weight_n = self.non_decimal.sub('', __weight)
            if 'lb' in __weight or 'lbs' in __weight:
                try:
                    weight = float(__weight_n) * 0.453592
                except ValueError:
                    return False, f"Bad Weight: {__weight}"
            else:
                try:
                    weight = float(__weight_n)
                except ValueError:
                    return False, f"Bad Weight: {__weight}"

        retval = {
            "height": height,
            "weight": weight,
            "blood_type": kwargs['blood_type']
        }

        return True, retval

    def create(self, *args, **kwargs):
        return super(BiometricManager, self).create(*args, **kwargs)
