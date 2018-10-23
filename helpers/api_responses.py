from rest_framework import status
from django.utils.translation import gettext as _

API_RESPONSES = {
    'errors': {
        '404': {
            'status': status.HTTP_404_NOT_FOUND,
            'message': _('Resource not found')
        },
        '401': {
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': _('Unauthorized access')
        },
        '500': {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': _('Server error')
        }
    }
}