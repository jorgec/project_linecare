from django.db.models import Q
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from datesdim.serializers import DateDimSerializer, TimeDimSerializer
from doctor_profiles.constants import QUEUE_DISPLAY_CODES, QUEUE_CANCELLED_CODES
from doctor_profiles.models import DoctorSchedule, DoctorProfile, MedicalInstitution
from doctor_profiles.models.doctor_schedule_models import DoctorScheduleDay, PatientAppointment
from doctor_profiles.models.managers.doctor_schedule_manager import check_collisions, find_gaps
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from doctor_profiles.modules.notifiers.doctor_appointment_notifiers import doctor_notify_new_appointment, \
    doctor_notify_update_queue
from doctor_profiles.serializers import DoctorScheduleSerializer, \
    MedicalInstitutionSerializer, PatientQueuePrivateSerializer
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
    include_past=yes
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('id', None))
        mi = request.GET.get('medical_institution', None)
        if mi:
            medical_institution = get_object_or_404(MedicalInstitution, id=mi)
        else:
            medical_institution = None

        if request.GET.get('include_past', 'no') == 'yes':
            serializer = DoctorScheduleSerializer(
                doctor.get_schedules(medical_institution=medical_institution, include_past=True), many=True)
        else:
            serializer = DoctorScheduleSerializer(doctor.get_schedules(medical_institution=medical_institution),
                                                  many=True)

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

        schedule_time_start = None
        schedule_time_end = None

        patient_id = request.data.get("profile_id", None)
        if not patient_id:
            return Response("No patient selected", status=status.HTTP_400_BAD_REQUEST)

        patient = get_object_or_404(BaseProfile, id=patient_id)

        schedule_choice = request.data.get('schedule_choice', 'first_available')
        preferred_day = request.data.get('appointment_day', None)
        if preferred_day:
            schedule_day = DateDim.objects.parse_get(preferred_day)
            if not schedule_day:
                return Response("Please set a date", status=status.HTTP_400_BAD_REQUEST)
        else:
            schedule_day = DateDim.objects.today()

        existing_schedules = DoctorScheduleDay.objects.filter(
            doctor=doctor,
            medical_institution=medical_institution,
            day=schedule_day
        ).order_by('schedule__start_time__minutes_since')

        if existing_schedules.count() == 0:
            return Response(f"{doctor} does not have a schedule for this day in {medical_institution}!",
                            status=status.HTTP_404_NOT_FOUND)

        existing_appointments = PatientAppointment.objects.filter(
            schedule_day=schedule_day,
            doctor=doctor,
            medical_institution=medical_institution,
        )

        """
        appointment type
        """
        appointment_type = request.data.get('appointment_type', 'Check Up')
        if schedule_choice == 'user_select':
            _schedule_time_start = request.data.get('appointment_time_start', None)
            if not _schedule_time_start:
                return Response("Please set a start time", status=status.HTTP_400_BAD_REQUEST)

            _schedule_time_end = request.data.get('appointment_time_end', None)
            if not _schedule_time_end:
                return Response("Please set a end time", status=status.HTTP_400_BAD_REQUEST)

            schedule_time_start = TimeDim.objects.parse(_schedule_time_start)
            schedule_time_end = TimeDim.objects.parse(_schedule_time_end)


        elif schedule_choice == 'first_available':
            schedule_options = doctor.get_options('schedule_options')
            if not f'{appointment_type}_duration' in schedule_options:
                return Response("Invalid appointment type", status=status.HTTP_400_BAD_REQUEST)

            first_available_result, schedule_time_start, schedule_time_end = find_gaps(
                schedules=existing_schedules,
                appointments=existing_appointments,
                duration=schedule_options[f'{appointment_type}_duration'],
                gap=schedule_options[f'{appointment_type}_gap']
            )

            if not first_available_result:
                return Response(
                    "We couldn't find an available slot; you can try manually setting your appointment times if you wish",
                    status=status.HTTP_409_CONFLICT)

        if not schedule_time_start or not schedule_time_end:
            return Response(f'{schedule_time_start} - {schedule_time_end} are invalid times!',
                            status=status.HTTP_400_BAD_REQUEST)

        """
        collision checks
        """
        # check if doc has schedule on that time

        valid_times = existing_schedules.filter(
            schedule__start_time__minutes_since__lte=schedule_time_start.minutes_since,
            schedule__end_time__minutes_since__gte=schedule_time_end.minutes_since
        )

        if valid_times.count() == 0:
            return Response(f"{doctor} does not have a schedule on that time!", status=status.HTTP_404_NOT_FOUND)

        # check available
        collisions = check_collisions(appointments=existing_appointments, schedule_time_start=schedule_time_start,
                                      schedule_time_end=schedule_time_end)

        if collisions.count() > 0:
            return Response("The schedule you want conflicts with an existing schedule!",
                            status=status.HTTP_409_CONFLICT)

        # all clear

        # schedule_day_object = DoctorScheduleDay.objects.get(doctor=doctor, medical_institution=medical_institution,
        #                                                     day=schedule_day)
        schedule_day_object = valid_times.first()
        appointment = PatientAppointment.objects.create(
            schedule_day=schedule_day,
            time_start=schedule_time_start,
            time_end=schedule_time_end,
            patient=patient,
            doctor=doctor,
            medical_institution=medical_institution,
            type=appointment_type,
            schedule_day_object=schedule_day_object
        )

        doctor_notify_new_appointment(appointment)

        # update queue number
        appointments_on_this_day = PatientAppointment.objects.filter(
            schedule_day_object=schedule_day_object
        ).order_by('time_start__minutes_since')

        queue_number = 1
        for a in appointments_on_this_day:
            a.queue_number = queue_number
            queue_number = queue_number + 1
            a.save()

        return Response(f"Appointment for {appointment} set", status=status.HTTP_200_OK)


class ApiPrivateDoctorScheduleQueueList(APIView):
    """
    Queue of doctor at medical institution on day
    ?doctor_id=doctor_id
    [optional]
    medical_institution_id=medical_institution_id
    date=YYYY-MM-DD
    count=n
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)

        if request.GET.get('medical_institution_id', None):
            medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('medical_institution_id', None))
            mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                          medical_institution=medical_institution, is_approved=True)
        else:
            medical_institution = None

        if type(profile_type) != DoctorProfile and medical_institution:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        if type(profile_type) == DoctorProfile and profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        __queue_date = request.GET.get('date', None)
        if not __queue_date:
            queue_date = DateDim.objects.today()
        else:
            if " " in __queue_date:
                __queue_date = __queue_date.split(" ")[0]
            queue_date = DateDim.objects.parse_get(__queue_date)
            if not queue_date:
                return Response(f"{__queue_date} is an invalid date", status=status.HTTP_400_BAD_REQUEST)


        if medical_institution:
            queue = PatientAppointment.objects.filter(
                status__in=QUEUE_DISPLAY_CODES,
                doctor=doctor,
                medical_institution=medical_institution,
                schedule_day=queue_date
            ).order_by('time_start__minutes_since')
        else:
            queue = PatientAppointment.objects.filter(
                status__in=QUEUE_DISPLAY_CODES,
                doctor=doctor,
                schedule_day=queue_date
            ).order_by('time_start__minutes_since')

        if request.GET.get('count', None):
            queue = queue[:int(request.GET.get('count', 1))]

        serializer = PatientQueuePrivateSerializer(queue, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateDoctorScheduleCalendar(APIView):
    """
    Get monthly schedule of doctor
    ?doctor_id=doctor_id&year=int&month=int
    [optional]
    medical_institution_id=medical_institution_id
    consumer=receptionist/doctor
    """

    permissions = [permissions.AllowAny]
    # permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_id = request.GET.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        year = request.GET.get('year', None)
        if not year:
            return Response("Year is required", status=status.HTTP_400_BAD_REQUEST)
        month = request.GET.get('month', None)
        if not month:
            return Response("Month is required", status=status.HTTP_400_BAD_REQUEST)

        consumer = 'doctor'

        """ Bypass """
        if not request.GET.get('darna', None):
            result, profile_type = is_doctor_or_receptionist(request.user)
            if not result:
                return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

            if profile_type == doctor:
                consumer = 'doctor'
            else:
                consumer = 'receptionist'

            if request.GET.get('medical_institution_id', None):
                medical_institution = get_object_or_404(MedicalInstitution,
                                                        id=request.GET.get('medical_institution_id', None))
                mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                                  medical_institution=medical_institution, is_approved=True)
            else:
                medical_institution = None

            if type(profile_type) != DoctorProfile:
                """ person adding isn't the doctor, so check if receptionist is allowed """
                connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile)
                if not connection:
                    return Response("Receptionist is not authorized by this doctor for this medical institution",
                                    status=status.HTTP_403_FORBIDDEN)
            elif profile_type.id != doctor.id:
                return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        events = []

        schedule_days = doctor.get_schedule_days_for_month(year=year, month=month)

        for schedule_day in schedule_days:
            start = f"{schedule_day.day}T{schedule_day.schedule.start_time}"
            end = f"{schedule_day.day}T{schedule_day.schedule.end_time}"
            if consumer == 'receptionist':
                base_url = reverse('receptionist_profile_doctor_queue', kwargs={
                    'medical_institution': schedule_day.medical_institution.slug,
                    'doctor_id': schedule_day.doctor_id
                })
            else:
                base_url = reverse('doctor_profile_schedule_detail', kwargs={
                    'medical_institution': schedule_day.medical_institution.slug
                })
            event = {
                "title": schedule_day.short(),
                "start": start,
                "end": end,
                "url": f"{base_url}?date={schedule_day.day}"
            }
            events.append(event)

        return Response(events, status=status.HTTP_200_OK)
