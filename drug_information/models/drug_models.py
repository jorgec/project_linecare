from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django_extensions.db import fields as extension_fields

from drug_information.models.constants import DRUG_MARKETING_STATUS
from drug_information.models.managers.drug_managers import GenericNameManager, ActiveIngredientManager, DrugManager


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
    name = models.CharField(max_length=512, unique=True)
    base_name = models.CharField(max_length=512)
    slug = extension_fields.AutoSlugField(populate_from="name", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    meta = JSONField(default=dict)

    is_generic = models.BooleanField(default=False)

    marketing_status = models.CharField(choices=DRUG_MARKETING_STATUS, default="HUMAN OTC DRUG", max_length=64,
                                        null=True, blank=True)
    route = ArrayField(base_field=models.CharField(max_length=64), default=list, null=True, blank=True)
    # active_ingredients = JSONField(default=dict, null=True, blank=True)
    pharm_class = JSONField(default=dict, null=True, blank=True)
    dosage_form = ArrayField(base_field=models.CharField(max_length=64, null=True, blank=True), blank=True, null=True,
                             default=list)

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
