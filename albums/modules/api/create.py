from rest_framework import parsers, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from albums.models import Album
from albums.modules.response_templates.photo import save_template
from albums.serializers import PhotoUploadSerializer, PhotoSerializer


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

        serializer = PhotoUploadSerializer(data={
            'photo': request.data['photo'],
            'caption': request.data['caption'],
        })


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
            print(serializer.errors)
            response_data = save_template(**{
                'as_json': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'request': request,
                'result': serializer.errors
            })
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
