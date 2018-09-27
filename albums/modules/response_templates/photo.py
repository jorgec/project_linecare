from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from albums.serializers import PhotoSerializer


def save_template(**kwargs):
    as_json = kwargs['as_json']
    status = kwargs['status']
    request = kwargs['request']
    result = kwargs['result']

    if status == HTTP_200_OK:
        message = 'Save successful'
        data = PhotoSerializer(result).data
    else:
        message = result
        data = request.data

    response = {
        'status': status,
        'message': message,
        'data': data
    }

    if as_json:
        return json.dumps(response)
    return response
