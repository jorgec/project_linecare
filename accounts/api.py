# from django.contrib.auth import login, authenticate
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.db import IntegrityError
from django.db.models import Q
from rest_auth.registration.views import SocialLoginView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account, SUPERADMIN, ADMIN
from accounts.serializers import AccountSerializer, AccountSerializerPublic, LoginSerializer, AccountRegisterSerializer

"""
========================================================================================
TODO: Retrieval
========================================================================================
- GetUserBy
    - PK
    - username
- GetUsersBy
    - user_type
    - parent
    - all
    - parent
"""


class ApiGetUserByPK(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        if pk:
            user = get_object_or_404(Account, pk=pk, is_active=True)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiGetUserByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)

        if username:
            user = get_object_or_404(Account, username=username, is_active=True)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetUsersByUserType(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)

        if user_type:
            users = Account.objects.filter(
                user_type=user_type,
            ).exclude(
                Q(user_type=SUPERADMIN) | Q(user_type=ADMIN)
            ).actives()

            serializer = AccountSerializerPublic(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetUsersByUserType(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)

        if user_type:
            users = Account.objects.filter(
                user_type=user_type,
            ).actives()

            serializer = AccountSerializer(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetUsers(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        users = Account.objects.exclude(
            Q(user_type=SUPERADMIN) | Q(user_type=ADMIN)
        ).actives()

        serializer = AccountSerializerPublic(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateGetUsers(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = Account.objects.actives()

        serializer = AccountSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiGetUsersByParent(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        parent = request.GET.get('parent', None)

        if parent:
            users = Account.objects.filter(parent_id=parent)

            serializer = AccountSerializerPublic(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


"""
========================================================================================
TODO: Authentication
========================================================================================
- Login
- Register
"""


class ApiLogin(APIView):
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
    def post(self, request, *args, **kwargs):
        serializer = AccountRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = Account.objects.create_user(
                username=serializer.data['username'],
                email=serializer.data['email'],
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name'],
                password=serializer.data['password']
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiFacebookLogin(SocialLoginView):
    metadata_class = FacebookOAuth2Adapter
