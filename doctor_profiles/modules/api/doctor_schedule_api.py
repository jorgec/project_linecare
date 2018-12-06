from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from doctor_profiles.models import DoctorSchedule
from doctor_profiles.serializers import DoctorScheduleCreateRegularScheduleSerializer, DoctorScheduleSerializer


class ApiDoctorScheduleCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        start_time = TimeDim.objects.parse(request.data.get('start_time'))
        end_time = TimeDim.objects.parse(request.data.get('start_time'))
        start_date = DateDim.objects.parse_get(request.data.get('start_date'))
        end_date = DateDim.objects.parse_get(request.data.get('end_date'))

        schedule_data = {
            'days': request.data.get('days').split(';'),
            'medical_institution_id': request.GET.get('medical_institution'),
            'start_time': start_time,
            'end_time': end_time,
            'start_date': start_date,
            'end_date': end_date,
            'doctor_id': request.user.doctorprofile.id
        }

        print(schedule_data)

        schedule = DoctorSchedule.objects.create(**schedule_data)
        schedule_serializer = DoctorScheduleSerializer(schedule)
        print(schedule_serializer.data)

        return Response(schedule_serializer.data,status.HTTP_200_OK)
