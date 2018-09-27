from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from accounts.models import Account
from profiles.modules.response_templates.profile import public_profile_template, private_profile_template


# Public

class ApiPublicProfileGetByPK(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        profile = public_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


class ApiPublicProfileGetByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        if not username:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, username=username)

        profile = public_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


class ApiPublicProfileGetByUserType(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)
        if not user_type:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        users = Account.objects.filter(user_type=user_type).actives()
        profiles = []
        for user in users:
            profile = public_profile_template(user)
            profiles.append(profile)

        return Response(profile, status=status.HTTP_200_OK)

class ApiPrivateProfileGetByPK(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        profile = private_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)

class ApiPrivateProfileGetByUsername(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        if not username:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, username=username)

        profile = private_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)