from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountWithProfileSerializerPrivate
from biometrics.models import Biometric


class ApiPatientSubAccountCreate(APIView):
    """
    Create a patient as a sub-account under the doctor or receptionist account
    """

    def post(self, request, *args, **kwargs):
        """
        1. create account using pseudo email and password
        2. populate base profile with provided info
        3. populate biometrics with provided info
        """

        formdata = {
            'height': request.data.get('height', None),
            'weight': request.data.get('weight', None),
            'blood_type': request.data.get('blood_type', None)
        }

        is_valid, bm_response = Biometric.objects.validate(**formdata)

        if is_valid:
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            date_of_birth = request.data.get('date_of_birth')
            gender_id = request.data.get('gender_id')

            user = Account.objects.create_sub_user(
                first_name=first_name,
                last_name=last_name,
                parent=request.user,
                date_of_birth=date_of_birth,
                gender_id=gender_id
            )
            bm = Biometric(
                height=bm_response['height'],
                weight=bm_response['weight'],
                blood_type=bm_response['blood_type'],
                user=user
            )
            bm.save()
            serializer = AccountWithProfileSerializerPrivate(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(bm_response, status=status.HTTP_400_BAD_REQUEST)
