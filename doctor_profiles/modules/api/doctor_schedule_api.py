from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from doctor_profiles.models import DoctorSchedule, DoctorProfile, MedicalInstitution
from doctor_profiles.serializers import DoctorScheduleCreateRegularScheduleSerializer, DoctorScheduleSerializer


class ApiDoctorScheduleCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctorprofile:
            return Response("Not a doctor", status=status.HTTP_403_FORBIDDEN)

        start_time = TimeDim.objects.parse(request.data.get('start_time'))
        end_time = TimeDim.objects.parse(request.data.get('end_time'))
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

        schedule = DoctorSchedule.objects.create(**schedule_data)
        schedule_serializer = DoctorScheduleSerializer(schedule)

        return Response(schedule_serializer.data, status.HTTP_200_OK)


class ApiDoctorScheduleList(APIView):
    """
    Get schedule list of doctor
    ?id=doctor_id
    [optional]

    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('id', None))
        mi = request.GET.get('medical_institution', None)
        if mi:
            medical_institution = get_object_or_404(MedicalInstitution, id=mi)
        else:
            medical_institution = None

        serializer = DoctorScheduleSerializer(doctor.get_schedules(medical_institution=medical_institution), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
