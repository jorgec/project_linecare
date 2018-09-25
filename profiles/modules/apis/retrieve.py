from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from accounts.constants import SUPERADMIN, ADMIN
from accounts.models import Account
from accounts.serializers import AccountWithProfileSerializerPrivate
from profiles.models import BaseProfile, ProfileMobtel, Gender
from profiles.modules.apis.return_templates import public_profile_template
from profiles.serializers import PublicProfileSerializer, PrivateMobtelSerializer, PrivateProfileSerializer


# Public

class ApiPublicGetProfileByPK(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        profile = public_profile_template(user)

        return Response(json.dumps(profile), status=status.HTTP_200_OK)


class ApiPublicGetProfileByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        if not username:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, username=username)

        profile = public_profile_template(user)

        return Response(json.dumps(profile), status=status.HTTP_200_OK)


class ApiPublicGetProfileByUserType(APIView):
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

        return Response(json.dumps(profiles), status=status.HTTP_200_OK)