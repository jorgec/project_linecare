from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from profiles.modules.response_templates.profile import update_template
from profiles.serializers import ProfileSerializer


class ApiPrivateProfileUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user.base_profile()

        serializer = ProfileSerializer(data=request.data, instance=profile)

        if serializer.is_valid():
            data = serializer.save()
            response_data = update_template(**{
                'as_json': False,
                'status': status.HTTP_200_OK,
                'request': request,
                'result': ProfileSerializer(data).data
            })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = update_template(**{
                'as_json': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'request': request,
                'result': serializer.errors
            })
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
