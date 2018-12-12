from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from doctor_profiles.models import DoctorSchedule, DoctorProfile, MedicalInstitution
from doctor_profiles.models.doctor_schedule_models import DoctorScheduleDay, PatientAppointment
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from doctor_profiles.serializers import DoctorScheduleSerializer, \
    MedicalInstitutionSerializer, DateDimSerializer, TimeDimSerializer
from profiles.models import BaseProfile
from receptionist_profiles.models import ReceptionistProfile


def is_doctor_or_receptionist(user):
    user_type = None
    try:
        doctor = DoctorProfile.objects.get(user=user)
        user_type = doctor
    except DoctorProfile.DoesNotExist:
        try:
            receptionist = ReceptionistProfile.objects.get(user=user)
            user_type = receptionist
        except ReceptionistProfile.DoesNotExist:
            return False, user_type
    return True, user_type


class ApiDoctorScheduleCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return Response("Doctor does not exist!", status=status.HTTP_404_NOT_FOUND)

        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution', None))

        mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                          medical_institution=medical_institution, is_approved=True)

        if type(profile_type) != DoctorProfile:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

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
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution', None))

        mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                          medical_institution=medical_institution, is_approved=True)

        if type(profile_type) != DoctorProfile:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        schedule = get_object_or_404(DoctorSchedule, id=request.GET.get('id', None), doctor=doctor)

        schedule.delete()

        return Response("Schedule deleted", status=status.HTTP_200_OK)


class ApiDoctorScheduleAppointmentCreate(APIView):
    """
    Create an appointment for doctor
    ?doctor_id=doctor_id&medical_institution_id=medical_institution_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution_id', None))

        mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                          medical_institution=medical_institution, is_approved=True)
        if type(profile_type) != DoctorProfile:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        """
        put this in a manager
        """
        preferred_schedule = request.data.get('schedule_date', None)
        if not preferred_schedule:
            return Response("Please set a date", status=status.HTTP_400_BAD_REQUEST)

        preferred_schedule_split = preferred_schedule.split(" ")

        schedule_day = DateDim.objects.parse_get(preferred_schedule_split[0])
        schedule_time_start = TimeDim.objects.parse(preferred_schedule_split[1])

        checkup_duration = doctor.get_options('checkup_duration') + doctor.get_options('checkup_gap')

        goes_past_midnight = False
        try:
            schedule_time_end = TimeDim.objects.get(minutes_since=schedule_time_start.minutes_since + checkup_duration)
        except TimeDim.DoesNotExist:
            goes_past_midnight = True
            mins_til_midnight = 1440 - schedule_time_start.minutes_since
            mins_past_midnight = checkup_duration - mins_til_midnight
            schedule_time_end = TimeDim.objects.get(minutes_since=mins_past_midnight)

        patient_id = request.data.get("profile_id", None)
        if not patient_id:
            return Response("No patient selected", status=status.HTTP_400_BAD_REQUEST)

        patient = get_object_or_404(BaseProfile, id=patient_id)

        """
        collision checks
        """
        # check if doc has schedule on this day
        existing_schedules = DoctorScheduleDay.objects.filter(
            doctor=doctor,
            medical_institution=medical_institution,
            day=schedule_day
        )
        if existing_schedules.count() == 0:
            return Response(f"{doctor} does not have a schedule for this day in {medical_institution}!",
                            status=status.HTTP_404_NOT_FOUND)

        # check if doc has schedule on that time
        if not goes_past_midnight:
            valid_times = existing_schedules.filter(
                schedule__start_time__minutes_since__lte=schedule_time_start.minutes_since,
                schedule__end_time__minutes_since__gte=schedule_time_end.minutes_since
            )
        else:
            valid_times = existing_schedules.filter(
                schedule__time_start__minutes_since__lte=schedule_time_start.minutes_since
            )

        if valid_times.count() == 0:
            return Response(f"{doctor} does not have a schedule on that time!", status=status.HTTP_404_NOT_FOUND)

        # check available
        collisions = PatientAppointment.objects.filter(
            schedule_day=schedule_day,
            doctor=doctor,
            medical_institution=medical_institution,
        ).filter(
            (Q(time_start__minutes_since__lte=schedule_time_start.minutes_since) & Q(
                time_end__minutes_since__gte=schedule_time_start.minutes_since)) |
            (Q(time_start__minutes_since__lte=schedule_time_end.minutes_since) & Q(
                time_end__minutes_since__gte=schedule_time_end.minutes_since)) |
            (Q(time_end__minutes_since__gte=schedule_time_start.minutes_since) & Q(
                time_end__minutes_since__lte=schedule_time_end.minutes_since)) |
            (Q(time_start__minutes_since__gte=schedule_time_start.minutes_since) & Q(
                time_end__minutes_since__lte=schedule_time_end.minutes_since))
        )

        if collisions.count() > 0:
            return Response("The schedule you want conflicts with an existing schedule!",
                            status=status.HTTP_409_CONFLICT)

        # all clear

        appointment = PatientAppointment.objects.create(
            schedule_day=schedule_day,
            time_start=schedule_time_start,
            time_end=schedule_time_end,
            patient=patient,
            doctor=doctor,
            medical_institution=medical_institution
        )

        return Response(f"Appointment for {appointment} set", status=status.HTTP_200_OK)
