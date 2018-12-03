from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import TimeDim
from doctor_profiles.serializers import DoctorScheduleCreateSerializer


class ApiDoctorScheduleCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        start_time = TimeDim.objects.parse(request.data.get('start_time', None))
        print(start_time)


        return Response(status.HTTP_200_OK)