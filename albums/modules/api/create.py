from rest_framework import parsers, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from albums.models import Album
from albums.serializers import PhotoUploadSerializer


class ApiPrivateAlbumPostUploadPhoto(APIView):
    """
    Upload a photo to a specified album (via pk)
    ?pk=<n>

    photo: file
    caption: string
    """
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=request.GET.get('pk', None), profile=request.user.base_profile())
        serializer = PhotoUploadSerializer(data=request.data)

        if serializer.is_valid():
            pass

