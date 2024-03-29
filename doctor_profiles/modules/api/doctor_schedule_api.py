import arrow
from django.conf import settings
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import TimeDim, DateDim
from datesdim.serializers import DateDimSerializer, TimeDimSerializer
from doctor_profiles.constants import QUEUE_DISPLAY_CODES, QUEUE_NOT_CANCELLED_BUT_NOT_DONE_CODES
from doctor_profiles.models import DoctorSchedule, DoctorProfile, MedicalInstitution
from doctor_profiles.models.doctor_schedule_models import DoctorScheduleDay, PatientAppointment
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from doctor_profiles.serializers import DoctorScheduleSerializer, \
    MedicalInstitutionSerializer, PatientQueuePrivateSerializer
from doctor_profiles.serializers.doctor_schedule_serializer import DoctorScheduleDayBasicSerializer, \
    DoctorScheduleListQueryParamsSerializer
from receptionist_profiles.models import ReceptionistProfile


def is_doctor_or_receptionist(user):
    """
    Check whether logged in user is a doctor or a receptionist

    Parameters:
    accounts.Account model

    Returns:
    bool, profile instance
    """
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
    """
    Create a doctor schedule
    Allows doctor or receptionist profile
    <br>
    <strong>POST PARAMS</STRONG>:
    - start_time: str HH:mm (24-hour format) or hh:mm a (12-hour format)
    - end_time: str HH:mm (24-hour format) or hh:mm a (12-hour format)
    - start_date: str YYYY-MM-DD
    - end_date: str YYYY-MM-DD
    - doctor_id: int
    - medical_institution_id: int
    - days: str 'Monday^Tuesday^...' (note: use caret ^ to split the days)

    <br>
    <strong>RESPONSE</strong>:
    - <em>SUCCESS</em>: status code: 201
    <pre>
    {
       id: int,
       start_time: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
       },
       end_time: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
       },
       start_date: DateDim{
            id: int
            year: int
            month: int
            day: int
            date_obj: datetime
            day_name: str
            week_day: int
            week_month: int
            week_year: int
            month_name: str
            month_name_short: str
            day_name_short: str
       },
       end_date: DateDim{
            id: int
            year: int
            month: int
            day: int
            date_obj: datetime
            day_name: str
            week_day: int
            week_month: int
            week_year: int
            month_name: str
            month_name_short: str
            day_name_short: str
       },
       doctor: DoctorProfile{
            id: int,
            created: datetime,
            last_updated: datetime,
            metadata: json,
            user: Account{
                id: int,
                username: str,
                user_type: int,
                base_profile: BaseProfile{
                    first_name: str,
                    last_name: str
                }
            },
            doctor_name: str
       },
       medical_institution: MedicalInstitution{
            id: int,
            slug: str,
            name: str,
            type: MedicalInstitutionType{
                id: int,
                name: str,
                slug: str,
                created: datetime,
                last_updated: datetime,
                metadata: json,
                is_approved: bool
            },
            coords: MedicalInstitutionCoordinate{
                lat: decimal,
                lon: decimal,
                created: datetime,
                last_updated: datetime,
                metadata: json,
                is_approved: bool,
                medical_institution: int,
                suggested_by: int (Account id),
                address: {
                       id: int,
                       zip_code: int,
                       country: Country{
                            id: int,
                            iso: str,
                            name: str,
                            slug: str,
                            nicename: str,
                            iso3: str,
                            numcode: int,
                            phonecode: int
                       },
                       region: Region{
                            id: int,
                            slug: str,
                            name: str
                       },
                       province: Province{
                            id: int,
                            slug: str,
                            name: str
                       },
                       city: City{
                            id: int,
                            slug: str,
                            name: str
                       },
                       address: str
                },
            }
       },
       days_split: str (comma separated list of days),
       mi_queue: str (URL for the queue)
    }
    </pre>
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.data.get('doctor_id', None)
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return Response("Doctor does not exist!", status=status.HTTP_404_NOT_FOUND)

        medical_institution = get_object_or_404(MedicalInstitution, id=request.data.get('medical_institution_id', None))

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
        days = request.data.get('days').split('^')
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

            return Response(schedule_serializer.data, status.HTTP_201_CREATED)
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
            elif message == "Invalid start and end dates":
                return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ApiDoctorScheduleDayList(APIView):
    """
    Get days of particular schedule
    <br>
    <strong>GET PARAMS</strong>:
    - id: int (schedule_id)

    <br>
    <strong>RESPONSE</strong>:
    - <em>SUCCESS</em>: status code: 200
    <pre>
    {
        id: int,
        actual_start_time: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
       },
       actual_end_time: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
       },
       day: DateDim{
            id: int
            year: int
            month: int
            day: int
            date_obj: datetime
            day_name: str
            week_day: int
            week_month: int
            week_year: int
            month_name: str
            month_name_short: str
            day_name_short: str
       },
       doctor: int (DoctorProfile id),
       medical_institution: int (MedicalInstitution id),
       schedule: int (Schedule id),
       doctor_id_in: bool,
       doctor_stepped_out: bool
    }
    </pre>
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        schedule = get_object_or_404(DoctorSchedule, id=request.GET.get('id', None))
        schedule_days = schedule.get_schedule_days().order_by('day__date_obj')

        serializer = DoctorScheduleDayBasicSerializer(schedule_days, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiDoctorScheduleList(APIView):
    """
    Get schedule list of doctor

    Accept the following GET parameters: id, [medical_institution, include_past, filter_days]
    ?id=doctor_id
    [optional]
    medical_institution=medical_institution_id
    include_past=yes
    filter_days=Monday^Tuesday^...
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = DoctorScheduleListQueryParamsSerializer

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('id', None))
        mi = request.GET.get('medical_institution', None)
        if mi:
            medical_institution = get_object_or_404(MedicalInstitution, id=mi)
        else:
            medical_institution = None

        filter_days = request.GET.get('filter_days', None)
        if filter_days:
            days = request.GET.get('filter_days').split("^")
        else:
            days = None

        if request.GET.get('include_past', 'no') == 'yes':
            serializer = DoctorScheduleSerializer(
                doctor.get_schedules(
                    medical_institution=medical_institution,
                    include_past=True,
                    filter_days=days
                ), many=True)
        else:
            serializer = DoctorScheduleSerializer(doctor.get_schedules(
                medical_institution=medical_institution,
                filter_days=days
            ),
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

        schedule = get_object_or_404(DoctorSchedule, id=request.data.get('id', None))

        flag = False
        if type(profile_type) == DoctorProfile and profile_type == schedule.doctor:
            flag = True

        if type(profile_type) == ReceptionistProfile and schedule.doctor.verify_receptionist(receptionist=profile_type,
                                                                                             medical_institution=schedule.medical_institution):
            flag = True

        if flag:
            schedule.delete()
            return Response("Schedule deleted", status=status.HTTP_200_OK)
        else:
            return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)


class ApiDoctorScheduleAppointmentCreate(APIView):
    """
    Create an appointment for doctor
    <br>
    <strong>POST PARAMS</strong>:
    - doctor_id: int
    - medical_institution_id: int
    - profile_id: int (patient base_profile id)
    - appointment_day: str (YYYY-MM-DD)
    - appointment_type: "checkup"|"followup"|"lab_result"|"consultation"
    [[ optional ]]
    - force_schedule: "true"|"false" (doctor or receptionist only)
    - schedule_choice: "first_available"|"user_select" (default: first available)
    - appointment_time_start: str (HH:mm)
    - appointment_time_end: str (HH:mm)
    - schedule_day_id: int (used if force_schedule == "true")

    <br>
    <strong>RESPONSE</strong>:
    - <em>SUCCESS</em>: status code: 201
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        medical_institution = get_object_or_404(MedicalInstitution, id=request.data.get('medical_institution_id', None))

        mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                          medical_institution=medical_institution, is_approved=True)

        """ kwargs """
        patient_id = request.data.get("profile_id", None)
        force_schedule = request.data.get('force_schedule', False)
        schedule_choice = request.data.get('schedule_choice', 'first_available')
        preferred_day = request.data.get('appointment_day', None)
        preferred_time_start = request.data.get('appointment_time_start', None)
        preferred_time_end = request.data.get('appointment_time_end', None)
        appointment_type = request.data.get('appointment_type', 'checkup')
        schedule_day_id = request.data.get('schedule_day_id', None)
        """ /kwargs """

        if force_schedule == 'true':
            result, profile_type = is_doctor_or_receptionist(request.user)
            if not result:
                return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

            if type(profile_type) != DoctorProfile:
                """ person adding isn't the doctor, so check if receptionist is allowed """
                connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                        medical_institution=medical_institution)
                if not connection:
                    return Response("Receptionist is not authorized by this doctor for this medical institution",
                                    status=status.HTTP_403_FORBIDDEN)
            elif profile_type.id != doctor.id:
                return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

            force_schedule = True
        else:
            force_schedule = False

        create_result, appointment, status_code = PatientAppointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor.id,
            medical_institution_id=medical_institution.id,
            appointment_day=preferred_day,
            preferred_time_start=preferred_time_start,
            preferred_time_end=preferred_time_end,
            schedule_choice=schedule_choice,
            force_schedule=force_schedule,
            appointment_type=appointment_type,
            schedule_day_id=schedule_day_id
        )

        if create_result:

            # update queue number
            appointments_on_this_day = PatientAppointment.objects.filter(
                schedule_day_object=appointment.schedule_day_object
            ).order_by('time_start__minutes_since')

            queue_number = 1
            for a in appointments_on_this_day:
                a.queue_number = queue_number
                queue_number = queue_number + 1
                a.save()

            return Response(f"Appointment for {appointment} set", status=status_code)
        else:
            return Response(appointment, status=status_code)


class ApiPrivateDoctorScheduleDayPresenceStatus(APIView):
    """
    Check whether doctor is in or out
    ?schedule_day=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        schedule_day = get_object_or_404(DoctorScheduleDay, id=request.GET.get('schedule_day'))

        if schedule_day.doctor_is_in:
            button_classes = 'btn btn-success'
            button_text = 'In'
        else:
            button_classes = 'btn btn-danger'
            button_text = 'Out'

        button_href = f"{reverse('api_private_doctor_schedule_day_presence_toggle')}?schedule_day={schedule_day.id}"

        return Response({
            'button_href': button_href,
            'button_classes': button_classes,
            'button_text': button_text,
            'status': schedule_day.doctor_is_in
        }, status=status.HTTP_200_OK)


class ApiPrivateDoctorScheduleDayPresenceToggle(APIView):
    """
    Toggle doctor is in or not
    ?schedule_day=n
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        schedule_day = get_object_or_404(DoctorScheduleDay, id=request.GET.get('schedule_day'))
        doctor = schedule_day.doctor
        medical_institution = schedule_day.medical_institution

        if type(profile_type) != DoctorProfile:
            """ person adding isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        else:
            if doctor != request.user.doctor_profile():
                return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        now = TimeDim.objects.parse(arrow.utcnow().to(settings.TIME_ZONE).datetime)

        if schedule_day.doctor_is_in:
            if not schedule_day.actual_end_time:
                schedule_day.doctor_is_in = False
                schedule_day.actual_end_time = now
                message = 'Successfully checked out'
            else:
                message = 'You have already checked out!'
        else:
            if not schedule_day.actual_start_time:
                schedule_day.doctor_is_in = True
                schedule_day.actual_start_time = now
                message = 'Successfully checked in'
            else:
                message = 'You have already checked in!'

        schedule_day.save()

        return Response({
            'status': schedule_day.doctor_is_in,
            'message': message
        }, status=status.HTTP_200_OK)


class ApiPublicDummyScheduleQueueList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        queue = PatientAppointment.objects.filter(
            status__in=QUEUE_DISPLAY_CODES,
        ).order_by('time_start__minutes_since')[:10]

        serializer = PatientQueuePrivateSerializer(queue, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateDoctorScheduleQueueList(APIView):
    """
    Queue of doctor at medical institution on day
    <strong>GET PARAMS</strong>:
    - doctor_id: int
    [optional]
    date: str (YYYY-MM-DD)
    count: int
    [[ mutually exclusive ]]
    medical_institution_id: int
    - or -
    schedule_id: int (overrides medical_institution_id)

    <strong>RESPONSE</strong>:
    - <em>SUCCESS</em>: status code: 200
    <pre>
    {
        id: int,
        metadata: json,
        status: str,
        schedule_day: DateDim{
            id: int
            year: int
            month: int
            day: int
            date_obj: datetime
            day_name: str
            week_day: int
            week_month: int
            week_year: int
            month_name: str
            month_name_short: str
            day_name_short: str
        },
        time_start: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
        },
        time_end: TimeDim{
            hour: int,
            minute: int,
            minutes_since: int,
            format_24: str,
            format_12: str
        },
        patient: BaseProfile{
            id: int,
            first_name: str,
            last_name: str,
            gender: Gender{
                name: str,
                slug: str
            }
            date_of_birth: str (YYYY-MM-DD),
            profile_photo: str (url)
            profile_photo_css: str (css rule: background-img: url()),
            full_name: str,
            patient_detail_url: str (url)
        },
        doctor: int,
        medical_institution: MedicalInstitution{
            id: int,
            slug: str,
            name: str,
            type: MedicalInstitutionType{
                id: int,
                name: str,
                slug: str,
                created: datetime,
                last_updated: datetime,
                metadata: json,
                is_approved: bool
            },
            coords: MedicalInstitutionCoordinate{
                lat: decimal,
                lon: decimal,
                created: datetime,
                last_updated: datetime,
                metadata: json,
                is_approved: bool,
                medical_institution: int,
                suggested_by: int (Account id),
                address: {
                       id: int,
                       zip_code: int,
                       country: Country{
                            id: int,
                            iso: str,
                            name: str,
                            slug: str,
                            nicename: str,
                            iso3: str,
                            numcode: int,
                            phonecode: int
                       },
                       region: Region{
                            id: int,
                            slug: str,
                            name: str
                       },
                       province: Province{
                            id: int,
                            slug: str,
                            name: str
                       },
                       city: City{
                            id: int,
                            slug: str,
                            name: str
                       },
                       address: str
                },
            }
        },
        schedule_day_object: int,
        prior_visits: int,
        type: str,
        queue_status: str,
        queue_number: int,
        status_display: str,
        last_visit: {
            date: str (YYYY-MM-DD),
            id: int (visit id),
            url: str (url)
        },
        patient_url: str (url),
        schedule: int or None,
        biometrics: Biometric{
            height: float,
            weight: float,
            blood_type: str

        }
    }
    </pre>
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.GET.get('doctor_id', None)
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)

        if request.GET.get('medical_institution_id', None):
            medical_institution = get_object_or_404(MedicalInstitution,
                                                    id=request.GET.get('medical_institution_id', None))
            mi_connection = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor,
                                              medical_institution=medical_institution, is_approved=True)
        else:
            medical_institution = None

        schedule_id = request.GET.get('schedule_id', None)

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

        if schedule_id:
            queue = PatientAppointment.objects.filter(
                status__in=QUEUE_DISPLAY_CODES,
                doctor=doctor,
                schedule_day=queue_date,
                schedule_day_object__schedule__id=schedule_id
            ).order_by('time_start__minutes_since')
        else:
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

    permission_classes = [permissions.AllowAny]

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
                "schedule_day_id": schedule_day.id,
                "doctor_id": schedule_day.doctor.id,
                "title": schedule_day.short(),
                "start": start,
                "end": end,
                "days": schedule_day.schedule.split_days(),
                "patient_count": schedule_day.day_schedule_object_patients.filter(
                    status__in=QUEUE_NOT_CANCELLED_BUT_NOT_DONE_CODES).count(),
                "url": f"{base_url}?date={schedule_day.day}",
                "delete_url": f"{reverse('api_private_doctor_schedule_day_delete')}"
            }
            events.append(event)

        return Response(events, status=status.HTTP_200_OK)


class ApiDoctorScheduleDayDelete(APIView):
    """
    Delete specific schedule on day

    : post :
    doctor_id=doctor_id
    id=schedule_day_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        schedule_day = DoctorScheduleDay.objects.get(id=request.data.get('schedule_day_id'))

        if schedule_day.day.date_obj < DateDim.objects.today().date_obj:
            return Response("You can't delete past schedules!", status=status.HTTP_400_BAD_REQUEST)

        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.data.get('doctor_id', None)
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return Response("Doctor does not exist!", status=status.HTTP_404_NOT_FOUND)

        medical_institution = schedule_day.medical_institution

        if type(profile_type) != DoctorProfile:
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile,
                                                    medical_institution=medical_institution)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        schedule_day.delete()

        return Response(f"{schedule_day} deleted!", status=status.HTTP_200_OK)
