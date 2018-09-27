from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from accounts.constants import USER_TYPE_CHOICES, USER_TYPES_TO_TEST
from accounts.models import Account
from albums.serializers import AlbumSerializer
from profiles.modules.response_templates.profile import public_profile_template, private_profile_template


# Public

class ApiPublicProfileGetByPK(APIView):
    """
    Get a user's public profile via PK
    ?pk=<pk>
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        if not pk:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, pk=pk)

        profile = public_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


class ApiPublicProfileGetByUsername(APIView):
    """
    Get a user's public profile via username
    ?username=<username>
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        if not username:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, username=username)

        profile = public_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


class ApiPublicProfileGetByUserType(APIView):
    """
    List of all users of a given user type
    ?user_type=<n>
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)
        if not user_type:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)
        user_type = int(user_type)

        found = False
        for t in USER_TYPES_TO_TEST:
            if user_type == t[0]:
                found = True
                break
        if not found:
            return Response('No such user type', status.HTTP_404_NOT_FOUND)

        users = Account.objects.filter(user_type=user_type).actives()
        profiles = []
        for user in users:
            profile = public_profile_template(user)
            profiles.append(profile)

        return Response(profiles, status=status.HTTP_200_OK)


# Private

class ApiPrivateProfileGetByPK(APIView):
    """
    Get a user's private profile via pk
    ?pk=<pk>
    """
    permission_classes = [permissions.IsAuthenticated]


        user = get_object_or_404(Account, pk=pk)

        profile = private_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


class ApiPrivateProfileGetByUsername(APIView):
    """
        Get a user's private profile via username
        ?username=<username>
        """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        if not username:
            return Response('KeyError', status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Account, username=username)

        profile = private_profile_template(user)

        return Response(profile, status=status.HTTP_200_OK)


