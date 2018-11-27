from django.contrib.postgres.fields import JSONField
from django.db import models as models


class ReceptionistProfile(models.Model):
    """
    The core Receptionist profile
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    user = models.OneToOneField('accounts.Account', related_name='receptionistprofile', on_delete=models.CASCADE,
                                null=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.user}'