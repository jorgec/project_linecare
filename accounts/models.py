from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from rest_framework.authtoken.models import Token

"""
Change user types based on project
"""
SUPERADMIN = 10401
ADMIN = 12482
USER = 16265
USER_CHILD = 24749
PROVIDER = 18359
PROVIDER_CHILD = 12733

USER_TYPE_CHOICES = (
    (SUPERADMIN, 'Super User'),
    (ADMIN, 'Admin'),
    (USER, 'User'),
    (USER_CHILD, 'User Child'),
    (PROVIDER, 'Provider'),
    (PROVIDER_CHILD, 'Provider Child')
)

USER_TYPES_TO_TEST = (
    (USER, 'User'),
    (USER_CHILD, 'User Child'),
    (PROVIDER, 'Provider'),
    (PROVIDER_CHILD, 'Provider Child')
)

USERNAME_REGEX = "^[a-zA-Z0-9.-]*$"


class AccountQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class AccountManager(BaseUserManager):
    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def create_user(self, email, username=None, password=None, user_type=USER, first_name='', last_name=''):
        if not username:
            username = slugify(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.user_type = SUPERADMIN
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username can only contain alphanumeric characters and the following characters: . -',
                code='Invalid Username'
            )
        ],
        unique=False,

    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=None, null=True, blank=True)
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    parent = models.ForeignKey("self", null=True, blank=True, related_name="account_children", on_delete=models.CASCADE)

    children = []
    parents = []

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
