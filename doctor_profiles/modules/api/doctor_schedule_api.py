from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from doctor_profiles.models import DoctorSchedule, DoctorProfile, MedicalInstitution
from doctor_profiles.serializers import DoctorScheduleCreateRegularScheduleSerializer, DoctorScheduleSerializer, \
    DoctorScheduleCollisionSerializer, MedicalInstitutionSerializer, DateDimSerializer, TimeDimSerializer


class ApiDoctorScheduleCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctorprofile and not request.user.receptionistprofile:
            return Response("Not a doctor or receptionist", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        if not doctor_id:
            if not request.user.doctorprofile:
                return Response("Not a doctor", status=status.HTTP_403_FORBIDDEN)
            doctor_id = request.user.doctorprofile.id

        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution'))

        if request.user.doctorprofile.id != doctor_id:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)

        start_time = TimeDim.objects.parse(request.data.get('start_time'))
        end_time = TimeDim.objects.parse(request.data.get('end_time'))
        start_date = DateDim.objects.parse_get(request.data.get('start_date'))
        end_date = DateDim.objects.parse_get(request.data.get('end_date'))
        days = request.data.get('days').split(';')
        if days == ['']:
            return Response("Which days should this schedule be applied to?", status=status.HTTP_400_BAD_REQUEST)

        schedule_data = {
            'days': days,
            'medical_institution': medical_institution,
            'start_time': start_time,
            'end_time': end_time,
            'start_date': start_date,
            'end_date': end_date,
            'doctor': doctor,
            'created_by': request.user
        }

        result, message, schedule = DoctorSchedule.objects.create(**schedule_data)
        if result:
            schedule_serializer = DoctorScheduleSerializer(schedule)
            return Response(schedule_serializer.data, status.HTTP_200_OK)
        else:
            if message == "Schedule Conflict":
                conflict_data = []
                for conflict in schedule:
                    d = {
                        'medical_institution': MedicalInstitutionSerializer(conflict['medical_institution']).data,
                        'day': DateDimSerializer(conflict['day']).data,
                        'schedule': DoctorScheduleSerializer(conflict['schedule']).data,
                        'start_time': TimeDimSerializer(conflict['start_time']).data,
                        'end_time': TimeDimSerializer(conflict['end_time']).data
                    }
                    conflict_data.append(d)

                return Response(conflict_data, status=status.HTTP_409_CONFLICT)
            elif message == "Invalid start and end time":
                return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ApiDoctorScheduleList(APIView):
    """
    Get schedule list of doctor
    ?id=doctor_id
    [optional]
    medical_institution=medical_institution_id
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


class ApiDoctorScheduleDelete(APIView):
    """
    Delete schedule
    ?id=schedule_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctorprofile and not request.user.receptionistprofile:
            return Response("Not a doctor or receptionist", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        if not doctor_id:
            if not request.user.doctorprofile:
                return Response("Not a doctor", status=status.HTTP_403_FORBIDDEN)
            doctor_id = request.user.doctorprofile.id

        doctor = get_object_or_404(DoctorProfile, id=doctor_id)

        schedule = get_object_or_404(DoctorSchedule, id=request.GET.get('id', None), doctor=doctor)

        schedule.delete()

        return Response("Schedule deleted", status=status.HTTP_200_OK)
