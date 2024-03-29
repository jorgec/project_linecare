from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from accounts.constants import SUPERADMIN, ADMIN
from accounts.models import Account
from accounts.serializers import AccountSerializer, AccountSerializerPublic

"""
========================================================================================
Retrieval
========================================================================================
- GetUserBy
    - PK (private)
    - username (public)
    - email (private)
- GetUsersBy
    - user_type (public/admin)
    - parent (public/private)
    - all (public/private)
"""

class ApiPrivateAccountGetByToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', None)

        if token:
            token = get_object_or_404(Token, key=token)
            user = get_object_or_404(Account, pk=token.user_id)
            serializer = AccountSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class ApiPublicAccountGetByToken(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', None)

        if token:
            token = get_object_or_404(Token, key=token)
            user = get_object_or_404(Account, pk=token.user_id)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class ApiPrivateAccountGetByPK(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        if pk:
            user = get_object_or_404(Account, pk=pk, is_active=True)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicAccountGetByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)

        if username:
            user = get_object_or_404(Account, username=username, is_active=True)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateAccountGetByEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            user = get_object_or_404(Account, email=email, is_active=True)

            serializer = AccountSerializerPublic(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicAccountsGetByUserType(APIView):
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


class ApiPrivateAccountsGetByUserType(APIView):
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


class ApiPublicAccountsGetAll(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        users = Account.objects.exclude(
            Q(user_type=SUPERADMIN) | Q(user_type=ADMIN)
        ).actives()

        serializer = AccountSerializerPublic(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiAdminAccountsGetAll(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = Account.objects.actives()

        serializer = AccountSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicAccountsGetByParent(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        parent = request.GET.get('parent', None)

        if parent:
            users = Account.objects.filter(parent_id=parent)

            serializer = AccountSerializerPublic(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)