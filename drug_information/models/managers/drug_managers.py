from django.db import models


class GenericNameManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(GenericNameManager, self).create(*args, **kwargs)



class ActiveIngredientManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(ActiveIngredientManager, self).create(*args, **kwargs)


class DrugManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(DrugManager, self).create(*args, **kwargs)


class DrugRouteManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(DrugRouteManager, self).create(*args, **kwargs)


class PharmaceuticalClassManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PharmaceuticalClassManager, self).create(*args, **kwargs)


class DosageFormManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(DosageFormManager, self).create(*args, **kwargs)
