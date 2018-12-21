from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django_extensions.db import fields as extension_fields

from drug_information.models.constants import DRUG_MARKETING_STATUS
from drug_information.models.managers.drug_managers import GenericNameManager, ActiveIngredientManager, DrugManager, \
    DosageFormManager, PharmaceuticalClassManager, DrugRouteManager


class GenericName(models.Model):
    # Fields
    name = models.CharField(max_length=512, unique=True)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    meta = JSONField(default=dict)

    objects = GenericNameManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f'{self.name}'


class Drug(models.Model):
    # Fields
    name = models.CharField(max_length=512)
    base_name = models.CharField(max_length=512)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    meta = JSONField(default=dict)

    is_generic = models.BooleanField(default=False)

    product_type = models.CharField(choices=DRUG_MARKETING_STATUS, default="HUMAN OTC DRUG", max_length=64,
                                        null=True, blank=True)

    openfda = JSONField(default=dict)
    packaging = JSONField(default=dict)

    # Relationship Fields
    generic_name = models.ForeignKey(GenericName, on_delete=models.SET_NULL, null=True, blank=True)

    objects = DrugManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f'{self.name}'


class ActiveIngredient(models.Model):
    # Fields
    name = models.CharField(max_length=512, unique=True)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    meta = JSONField(default=dict)

    objects = ActiveIngredientManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class DrugActiveIngredient(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    strength = models.CharField(max_length=64, null=True, blank=True)

    meta = JSONField(default=dict)

    # Relationship Fields
    drug = models.ForeignKey(Drug, related_name='drug_ingredients', on_delete=models.SET_NULL, null=True, blank=True)
    active_ingredient = models.ForeignKey(ActiveIngredient, related_name='ingredient_drugs', on_delete=models.SET_NULL,
                                          null=True, blank=True)

    class Meta:
        ordering = ('drug',)
        unique_together = ('drug', 'active_ingredient', 'strength')

    def __str__(self):
        return f'{self.drug}, {self.active_ingredient} {self.strength}'


class DrugRoute(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    name = models.CharField(max_length=512, unique=True)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)

    objects = DrugRouteManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DrugRouteDelivery(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    drug = models.ForeignKey(Drug, related_name='drug_routes', on_delete=models.CASCADE)
    route = models.ForeignKey(DrugRoute, related_name='route_drugs', on_delete=models.CASCADE)

    class Meta:
        ordering = ('route',)

    def __str__(self):
        return f'{self.route} - {self.drug}'


class PharmaceuticalClass(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    name = models.CharField(max_length=512, unique=True)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)

    objects = PharmaceuticalClassManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DrugPharmaceuticalClass(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    drug = models.ForeignKey(Drug, related_name='drug_pharmclass', on_delete=models.CASCADE)
    pharm_class = models.ForeignKey(PharmaceuticalClass, related_name='pharmclass_drugs', on_delete=models.CASCADE)

    class Meta:
        ordering = ('pharm_class',)

    def __str__(self):
        return f'{self.pharm_class} - {self.drug}'


class DosageForm(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    name = models.CharField(max_length=512, unique=True)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)

    objects = DosageFormManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DrugDosageForm(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    drug = models.ForeignKey(Drug, related_name='drug_dosageforms', on_delete=models.CASCADE)
    dosage_form = models.ForeignKey(DosageForm, related_name='dosageform_drugs', on_delete=models.CASCADE)

    class Meta:
        ordering = ('dosage_form',)

    def __str__(self):
        return f'{self.dosage_form} - {self.drug}'
