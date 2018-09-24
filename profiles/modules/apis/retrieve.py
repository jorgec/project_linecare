from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.constants import SUPERADMIN, ADMIN
from accounts.models import Account
from accounts.serializers import AccountWithProfileSerializerPrivate
from profiles.models import BaseProfile, ProfileMobtel, Gender
from profiles.serializers import PublicProfileSerializer, PrivateMobtelSerializer, PrivateProfileSerializer


class ApiPublicGetProfileByPK(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        if pk:
            user = get_object_or_404(Account, pk=pk)
            profile = user.account_profiles
            serializer = PublicProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetProfileByPK(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        if pk:
            user = get_object_or_404(Account, pk=pk)
            profile = get_object_or_404(BaseProfile, user=user.pk)
            mobtels = profile.profile_mobtels.all()

            profile_serializer = PrivateProfileSerializer(profile)
            mobtel_serializer = PrivateMobtelSerializer(mobtels, many=True)
            user_profile = {
                'profile': profile_serializer.data,
                'mobtels': mobtel_serializer.data
            }
            return Response(user_profile, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetProfileByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)

        if username:
            user = get_object_or_404(Account, username=username)
            profile = user.account_profiles
            serializer = PublicProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetProfileByUsername(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)

        if username:
            user = get_object_or_404(Account, username=username)
            profile = get_object_or_404(BaseProfile, user=user)
            mobtels = profile.profile_mobtels.all()

            profile_serializer = PrivateProfileSerializer(profile)
            mobtel_serializer = PrivateMobtelSerializer(mobtels, many=True)
            user_profile = {
                'profile': profile_serializer.data,
                'mobtels': mobtel_serializer.data,
            }

            return Response(user_profile, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetProfileByEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            user = get_object_or_404(Account, email=email, is_active=True)
            profile = user.account_profiles
            serializer = PublicProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetProfileByEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)

        if email:
            user = get_object_or_404(Account, email=email, is_active=True)
            profile = get_object_or_404(BaseProfile, user=user.pk)
            mobtels = profile.profile_mobtels.all()

            profile_serializer = PrivateProfileSerializer(profile)
            mobtel_serializer = PrivateMobtelSerializer(mobtels, many=True)
            user_profile = {
                'profile': profile_serializer.data,
                'mobtels': mobtel_serializer.data

            }
            return Response(user_profile, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetProfileByUserType(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)
        if user_type:
            users = Account.objects.filter(
                user_type=user_type,
            ).exclude(
                Q(user_type=SUPERADMIN) | Q(user_type=ADMIN)
            ).actives()

            serializer = PublicProfileSerializer(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetProfileByUserType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type', None)

        if user_type:
            users = Account.objects.filter(user_type=user_type)
            serializer = AccountWithProfileSerializerPrivate(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicGetProfileByGender(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        gender = request.GET.get('gender', None)
        if gender:
            users = Gender.objects.filter(
                slug=gender
            )
            serializer = PublicProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateGetProfileByGender(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        gender = request.GET.get('gender', None)
        if gender:
            users = Gender.objects.filter(
                slug=gender
            )
            serializer = PrivateProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class ApiPrivateGetAlbum(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        album = request.GET.get('album', None)
        if album:
            user = '' #Album.objects.filter()

            serializer = ApiPrivateGetAlbum(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


