import ast
from decimal import Decimal, InvalidOperation

import arrow
from arrow.parser import ParserError
from django.conf import settings
from django.db import models
from django_extensions.db import fields as extension_fields
from rest_framework.utils import json

VALUE_TYPES = (
    ('str', 'str'),
    ('int', 'int'),
    ('float', 'float'),
    ('decimal', 'decimal'),
    ('date', 'date'),
    ('datetime', 'datetime'),
    ('dict', 'dict'),
    ('list', 'list'),
    ('json', 'json')
)


class AppGlobalManager(models.Manager):
    def create(self, *, name, value, value_type):
        appsetting = self.model(
            name=name,
            value=value,
            value_type=value_type
        )
        appsetting.save(using=self._db)
        return appsetting


def return_formatter(appsetting):
    if appsetting.value_type == 'str':
        return appsetting.value

    if appsetting.value_type == 'int':
        try:
            return int(appsetting.value)
        except ValueError:
            return 0

    if appsetting.value_type == 'float':
        try:
            return float(appsetting.value)
        except ValueError:
            return 0.0

    if appsetting.value_type == 'decimal':
        try:
            return Decimal(appsetting.value)
        except InvalidOperation:
            return Decimal(0)

    if appsetting.value_type == 'date' or appsetting.value_type == 'datetime':
        try:
            return arrow.get(appsetting.value).to(settings.TIME_ZONE)
        except ParserError:
            return arrow.utcnow().to(settings.TIME_ZONE)

    if appsetting.value_type == 'dict':
        try:
            return ast.literal_eval(appsetting.value)
        except ValueError:
            return {}

    if appsetting.value_type == 'list':
        try:
            return ast.literal_eval(appsetting.value)
        except ValueError:
            return []

    if appsetting.value_type == 'json':
        try:
            return json.dumps(ast.literal_eval(appsetting.value))
        except ValueError:
            return json.dumps("")


class AppGlobal(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', unique=True)
    value = models.TextField(max_length=512)
    value_type = models.CharField(choices=VALUE_TYPES, default='int', max_length=20)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    objects = AppGlobalManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_value(self):
        return return_formatter(self)
