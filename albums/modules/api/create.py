from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import parsers, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Account
from albums.models import Album
from albums.modules.response_templates.photo import save_template
from albums.serializers import PhotoUploadSerializer, PhotoSerializer, AlbumCreateSerializer, AlbumSerializer, \
    SinglePhotoSerializer


class ApiPrivateAlbumCreate(APIView):
    """
    Create a generic album for logged-in user

    post:
        - name: str
        - is_public: bool
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AlbumCreateSerializer(data=request.data)

        if serializer.is_valid():
            v = serializer.validated_data
            album_data = {
                'name': v.get('name'),
                'is_public': v.get('is_public'),
                'profile': request.user.base_profile()
            }
            album = Album.objects.create(**album_data)
            response_serializer = AlbumSerializer(album)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errros, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivateAlbumPostUploadPhoto(APIView):
    """
    Upload a photo to a specified album (via pk)
    ?album=<pk>

    photo: file
    caption: string
    """
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        album = get_object_or_404(Album, pk=request.GET.get('album', None), profile=request.user.base_profile())

        # auth check
        if not album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        serializer = PhotoUploadSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save()
            photo.album = album
            photo.save()
            photo.set_primary_photo()

            response_data = save_template(**{
                'as_json': False,
                'status': status.HTTP_200_OK,
                'request': request,
                'result': PhotoSerializer(photo).data
            })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = save_template(**{
                'as_json': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'request': request,
                'result': serializer.errors
            })
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiPrivatePhotoViewSet(UserPassesTestMixin, ModelViewSet):
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer

    def test_func(self):
        try:
            album = Album.objects.get(pk=self.request.POST.get('album'))
        except Album.DoesNotExist:
            raise FileNotFoundError

        token = self.request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Account.objects.get(auth_token__key=token)

        if user.base_profile() != album.profile:
            raise PermissionDenied

        return True
