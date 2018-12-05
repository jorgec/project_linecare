from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from albums.models import Photo, Album
from albums.modules.response_templates.photo import save_template as photo_save_template
from albums.modules.response_templates.album import save_template as album_save_template

# album
from albums.serializers import AlbumUpdateSerializer, PhotoUpdateSerializer, PhotoSerializer


class ApiPrivateAlbumUpdate(APIView):
    """
    Update album data
    ?album=<pk>

    Fields:
    - name
    - description
    - is_public
    """

    permissions = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            album = get_object_or_404(Album, pk=request.GET.get('album', None))
        except AttributeError:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

        # auth check
        if not album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        serializer = AlbumUpdateSerializer(data=request.data, instance=album)

        if serializer.is_valid():
            result = serializer.update(album, serializer.validated_data)

            retstatus = status.HTTP_200_OK
        else:
            retstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
            result = serializer.errors

        retval = album_save_template(**{
            'as_json': False,
            'status': retstatus,
            'result': result,
            'request': request
        })

        return Response(retval, status=retstatus)


class ApiPrivateAlbumTogglePrivacy(APIView):
    """
    Toggle album's privacy settings
    ?album=<pk>
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            album = get_object_or_404(Album, pk=request.GET.get('album', None))
        except AttributeError:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

        # auth check
        if not album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        result = album.toggle_privacy()
        if result:
            retstatus = status.HTTP_200_OK
        else:
            retstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        retval = album_save_template(**{
            'as_json': False,
            'status': retstatus,
            'result': result,
            'request': request
        })

        return Response(retval, status=retstatus)


# photo

class ApiPrivatePhotoUpdate(APIView):
    """
    Update photo data
    ?photo=<pk>

    Fields:
    - caption
    """

    permissions = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            photo = get_object_or_404(Photo, pk=request.GET.get('photo', None))
        except AttributeError:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

        # auth check
        if not photo.album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        serializer = PhotoUpdateSerializer(data=request.data, instance=photo)

        if serializer.is_valid():
            result = serializer.update(photo, serializer.validated_data)
            retstatus = status.HTTP_200_OK
        else:
            retstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
            result = serializer.errors

        retval = photo_save_template(**{
            'as_json': False,
            'status': retstatus,
            'result': result,
            'request': request
        })

        return Response(retval, status=retstatus)


class ApiPrivateSetPrimaryPhoto(APIView):
    """
    Set photo as primary for album
    ?photo=<pk>
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            photo = get_object_or_404(Photo, pk=request.GET.get('photo', None))
        except AttributeError:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

        # auth check
        if not photo.album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        result = photo.set_primary_photo()
        if result:
            retstatus = status.HTTP_200_OK
            result = PhotoSerializer(result).data
        else:
            retstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        retval = photo_save_template(**{
            'as_json': False,
            'status': retstatus,
            'result': result,
            'request': request
        })

        return Response(retval, status=retstatus)


class ApiPrivatePhotoTogglePrivacy(APIView):
    """
    Toggle photo's privacy setting. Primary photos can't be made private
    ?photo=<pk>
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            photo = get_object_or_404(Photo, pk=request.GET.get('photo', None))
        except AttributeError:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

        # auth check
        if not photo.album.verify_ownership(request.user):
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        # /auth check

        result = photo.toggle_privacy()
        if result:
            retstatus = status.HTTP_200_OK
        else:
            retstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        retval = photo_save_template(**{
            'as_json': False,
            'status': retstatus,
            'result': result,
            'request': request
        })

        return Response(retval, status=retstatus)
