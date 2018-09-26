from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer, LoginSerializer, AccountRegisterSerializer

"""
========================================================================================
Authentication
========================================================================================
- Login
- Register
"""


class ApiLogin(APIView):
    """
    Login API
    - email
    - password
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user is not None:

                """
                generate additional return values here
                """
                retval = {
                    'message': 'Login Successful',
                    'user': AccountSerializer(user).data,
                    'token': Token.objects.get(user=user).key,
                    'status_code': status.HTTP_200_OK
                }

                return Response(retval, status=status.HTTP_200_OK)
            else:
                retval = {
                    'message': 'Authentication Failed',
                    'user': email,
                    'token': password,
                    'status_code': status.HTTP_401_UNAUTHORIZED
                }

                return Response(retval, status=status.HTTP_401_UNAUTHORIZED)
        else:
            retval = {
                'message': serializer.errors,
                'user': request.data.get('email'),
                'token': request.data.get('password'),
                'status_code': status.HTTP_400_BAD_REQUEST
            }

            return Response(retval, status=status.HTTP_400_BAD_REQUEST)


class ApiRegister(APIView):
    """
    Register API
        - email
        - password
        - username (optional)
    """
    def post(self, request, *args, **kwargs):
        serializer = AccountRegisterSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            try:
                username = serializer.data['username']
            except KeyError:
                username = None
            user = Account.objects.create_user(
                username=username,
                email=serializer.data['email'],
                password=serializer.data['password']
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiFacebookLogin(SocialLoginView):
    metadata_class = FacebookOAuth2Adapter
