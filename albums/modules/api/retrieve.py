from profile import Profile

from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from albums.models import Album
from albums.modules.response_templates.album import album_with_photos_template
from albums.serializers import AlbumSerializer, AlbumWithPhotosSerializer, PhotoSerializer


class ApiPublicAlbumsGetByUser(APIView):
    """
    Retrieve a list of albums by a user that are publicly visible
    ?user=<pk>
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, pk=request.GET.get('user', None))
        profile = user.base_profile()
        serializer = AlbumSerializer(profile.get_albums(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicAlbumGetByPK(APIView):
    """
    Retrieve a specific public album by pk
    ?album=<pk>
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=request.GET.get('album', None), is_public=True)
        photos = album.get_public_photos()
        obj = album_with_photos_template(album, photos)
        return Response(obj, status=status.HTTP_200_OK)


class ApiPrivateAlbumGetAlbums(APIView):
    """
    Get albums of currently logged in user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        albums = profile.get_albums()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateGetProfilePhotos(APIView):
    """
    Get profile photo album of currently logged in user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        album = profile.get_profile_album()
        if album:
            serializer = PhotoSerializer(album.album_photos.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)


class ApiPublicGetPhotos(APIView):
    """
    Get all public photos of an album
    ?id=album_id
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        album = get_object_or_404(Album, id=request.GET.get('id', None))

        serializer = PhotoSerializer(album.get_public_photos(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
