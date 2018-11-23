from django.db import models
from django.apps import apps


class MedicalInstitutionQuerySet(models.QuerySet):
    def by_region(self, *, region: int):
        return self.filter(
            medical_institution_locations__region_id=region
        )

    def by_province(self, *, province: int):
        return self.filter(
            medical_institution_locations__province_id=province
        )

    def by_city(self, *, city: int):
        return self.filter(
            medical_institution_locations__city_id=city
        )


class MedicalInstitutionManager(models.Manager):
    def get_queryset(self):
        return MedicalInstitutionQuerySet(self.model, using=self._db)

    def by_region(self, *, region: int):
        return self.get_queryset().by_region(region=region)
    
    def by_province(self, *, province: int):
        return self.get_queryset().by_province(province=province)
    
    def by_city(self, *, city: int):
        return self.get_queryset().by_city(city=city)


class MedicalInstitutionLocationManager(models.Manager):
    pass