from django.db import models
from django.apps import apps
from accounts.constants import DOCTOR, USER


class BaseProfileQuerySet(models.QuerySet):
    def doctors(self):
        return self.user.filter(user_type=DOCTOR)

    def users(self):
        return self.user.filter(user_type=USER)


class BaseProfileManager(models.Manager):
    def get_queryset(self):
        return BaseProfileQuerySet(self.model, using=self._db)

    def doctors(self):
        return self.get_queryset().doctors()

    def users(self):
        return self.get_queryset().users

    def create(self, *args, **kwargs):
        try:
            user = self.model.objects.get(user=kwargs['user'])
            return user
        except self.model.DoesNotExist:
            return super(BaseProfileManager, self).create(*args, **kwargs)
