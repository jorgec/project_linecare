"""
Change user types based on project
"""
SUPERADMIN = 10401
ADMIN = 12482
USER = 16265
USER_SUBACCOUNT = 24749
DOCTOR = 18359
DOCTOR_SUBACCOUNT = 12733

USER_TYPE_CHOICES = (
    (SUPERADMIN, 'Super User'),
    (ADMIN, 'Admin'),
    (USER, 'User'),
    (USER_SUBACCOUNT, 'User SubAccount'),
    (DOCTOR, 'Doctor'),
    (DOCTOR_SUBACCOUNT, 'Doctor SubAccount')
)

USER_TYPES_TO_TEST = (
    (USER, 'User'),
    (USER_SUBACCOUNT, 'User SubAccount'),
    (DOCTOR, 'Doctor'),
    (DOCTOR_SUBACCOUNT, 'Doctor SubAccount')
)

USERNAME_REGEX = "^[a-zA-Z0-9.-]*$"