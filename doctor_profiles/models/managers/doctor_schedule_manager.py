from _socket import gaierror

import arrow
from django.apps import apps
from django.conf import settings
from django.db import models as models, IntegrityError
from django.db.models import Q
from rest_framework import status

from doctor_profiles.constants import QUEUE_STATUS_MESSAGES, QUEUE_CANCELLED_CODES, QUEUE_INACTIVE
from profiles.notifiers.patient_appointment_notifiers import patient_appointment_status_notify

"""
Doctor Schedule helper functions
"""


def find_gaps(*, schedules, appointments, duration, gap):
    duration = int(duration)
    gap = int(gap)
    TimeDim = apps.get_model('datesdim.TimeDim')
    DateDim = apps.get_model('datesdim.DateDim')
    now = TimeDim.objects.parse(arrow.utcnow().to(settings.TIME_ZONE).datetime)
    today = DateDim.objects.today()
    for schedule in schedules:
        if (now.minutes_since > schedule.schedule.start_time.minutes_since) and schedule.day == today:
            start_time = now
        else:
            start_time = schedule.schedule.start_time
        end_time = TimeDim.objects.get(minutes_since=start_time.minutes_since + duration)
        while end_time.minutes_since < schedule.schedule.end_time.minutes_since:
            collisions = check_collisions(
                appointments=appointments,
                schedule_time_start=start_time,
                schedule_time_end=end_time
            )
            if collisions.count() == 0:
                return True, start_time, end_time
            else:
                start_time = TimeDim.objects.get(minutes_since=end_time.minutes_since + gap)
                end_time = TimeDim.objects.get(minutes_since=start_time.minutes_since + duration)
    return False, None, None


def check_collisions(*, appointments, schedule_time_start, schedule_time_end):
    return appointments.filter(
        (Q(time_start__minutes_since__lte=schedule_time_start.minutes_since) & Q(
            time_end__minutes_since__gte=schedule_time_start.minutes_since)) |
        (Q(time_start__minutes_since__lte=schedule_time_end.minutes_since) & Q(
            time_end__minutes_since__gte=schedule_time_end.minutes_since)) |
        (Q(time_end__minutes_since__gte=schedule_time_start.minutes_since) & Q(
            time_end__minutes_since__lte=schedule_time_end.minutes_since)) |
        (Q(time_start__minutes_since__gte=schedule_time_start.minutes_since) & Q(
            time_end__minutes_since__lte=schedule_time_end.minutes_since))
    ).exclude(
        status__in=QUEUE_CANCELLED_CODES
    )


class PatientAppointmentQuerySet(models.QuerySet):
    def prior_visits(self, *, doctor, patient):
        return self.filter(
            doctor=doctor,
            patient=patient,
        )

    def other_appointments(self, *, schedule_day, doctor, medical_institution, time_start=None, inactive_only=True):
        filters = {
            'schedule_day': schedule_day,
            'doctor': doctor,
            'medical_institution': medical_institution
        }

        if time_start:
            filters['time_start__minutes_since__gte'] = time_start.minutes_since

        if inactive_only:
            filters['status__in'] = QUEUE_INACTIVE

        return self.filter(**filters)


class PatientAppointmentManager(models.Manager):
    def get_queryset(self):
        return PatientAppointmentQuerySet(self.model, using=self._db)

    def get_other_appointments(self, *, instance, time_start=None, inactive_only=True):
        filters = {
            'schedule_day': instance.schedule_day,
            'doctor': instance.doctor,
            'medical_institution': instance.medical_institution,
        }
        if time_start:
            filters['time_start'] = time_start

        if inactive_only:
            filters['inactive_only'] = inactive_only
        return self.get_queryset().other_appointments(**filters)

    def update_start_times(self, instance, time_start=None):
        TimeDim = apps.get_model('datesdim.TimeDim')
        Conn = apps.get_model('doctor_profiles.MedicalInstitutionDoctor')
        now = arrow.utcnow().to(settings.TIME_ZONE)
        if not time_start:
            new_time_start = TimeDim.objects.parse(now.datetime)
        else:
            new_time_start = time_start

        affected_appointments = self.get_other_appointments(
            instance=instance,
            inactive_only=True
        ).order_by(
            'time_start__minutes_since'
        )

        for appointment in affected_appointments:
            if appointment == instance:
                pass
            else:
                appointment.shift_time(new_time_start)
            conn = Conn.objects.get(doctor=appointment.doctor, medical_institution=appointment.medical_institution)
            durations = conn.get_schedule_options()['durations']
            gap = int(durations[f'{appointment.type}_gap'])
            try:
                new_time_start = TimeDim.objects.get(minutes_since=appointment.time_end.minutes_since + gap)
            except TimeDim.DoesNotExist:
                return False

    def prior_visits(self, *, doctor, patient):
        return self.get_queryset().prior_visits(
            doctor=doctor,
            patient=patient,
        )

    def update_status(self, *, id, status):
        TimeDim = apps.get_model('datesdim.TimeDim')
        appointment = self.get(id=id)
        appointment.status = status
        if appointment.status == 'in_progress':
            appointment.shift_time()
            Conn = apps.get_model('doctor_profiles.MedicalInstitutionDoctor')
            conn = Conn.objects.get(doctor=appointment.doctor, medical_institution=appointment.medical_institution)
            durations = conn.get_schedule_options()['durations']
            gap = int(durations[f'{appointment.type}_gap'])
            try:
                new_time_start = TimeDim.objects.get(minutes_since=appointment.time_end.minutes_since + gap)
                self.update_start_times(appointment, time_start=new_time_start)
            except TimeDim.DoesNotExist:
                pass
        appointment.save()
        try:
            patient_appointment_status_notify(appointment,
                                              QUEUE_STATUS_MESSAGES[status]['message'],
                                              QUEUE_STATUS_MESSAGES[status]['color'])
        except gaierror:
            pass

    def get_existing_schedules(self, *, doctor, medical_institution, schedule_day):
        DoctorScheduleDay = apps.get_model('doctor_profiles.DoctorScheduleDay')
        existing_schedules = DoctorScheduleDay.objects.filter(
            doctor=doctor,
            medical_institution=medical_institution,
            day=schedule_day
        ).order_by('schedule__start_time__minutes_since')

        if existing_schedules.count() == 0:
            return False, f"{doctor} does not have a schedule for this day in {medical_institution}!"

        existing_appointments = self.get_queryset().filter(
            schedule_day=schedule_day,
            doctor=doctor,
            medical_institution=medical_institution,
        )

        return True, {'existing_appointments': existing_appointments, 'existing_schedules': existing_schedules}

    def get_schedule_times(self, *, schedule_choice, appointment_type=None, mi_connection=None, start=None, end=None,
                           existing_schedules=None, existing_appointments=None):
        TimeDim = apps.get_model('datesdim.TimeDim')

        if schedule_choice == 'user_select':
            _schedule_time_start = start
            if not _schedule_time_start:
                return False, "Please set a start time"

            _schedule_time_end = end
            if not _schedule_time_end:
                return False, "Please set a end time"
            schedule_time_start = TimeDim.objects.parse(_schedule_time_start)
            schedule_time_end = TimeDim.objects.parse(_schedule_time_end)

        else:
            # schedule_options = doctor.get_options('schedule_options')
            schedule_options = mi_connection.get_schedule_options()['durations']
            if not f'{appointment_type}_duration' in schedule_options:
                return False, {'schedule_time_start': start, 'schedule_time_end': end}, "Invalid appointment type"

            first_available_result, schedule_time_start, schedule_time_end = find_gaps(
                schedules=existing_schedules,
                appointments=existing_appointments,
                duration=schedule_options[f'{appointment_type}_duration'],
                gap=schedule_options[f'{appointment_type}_gap']
            )

            if not first_available_result:
                return False, {'schedule_time_start': schedule_time_start, 'schedule_time_end': schedule_time_end}, "We couldn't find an available slot; you can try manually setting your appointment times if you wish"

        if not schedule_time_start:
            return False, {'schedule_time_start': schedule_time_start, 'schedule_time_end': schedule_time_end}, f"{schedule_time_start} is not a valid time"

        if not schedule_time_end:
            return False, {'schedule_time_start': schedule_time_start, 'schedule_time_end': schedule_time_end}, f"{schedule_time_end} is not a valid time"

        return True, {'schedule_time_start': schedule_time_start, 'schedule_time_end': schedule_time_end}, ""

    def is_doctor_or_receptionist(self, user):
        DoctorProfile = apps.get_model('doctor_profiles.DoctorProfile')
        ReceptionistProfile = apps.get_model('receptionist_profiles.ReceptionistProfile')

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

    def collision_checks(self, *, force_schedule=False, schedule_day_id=None, schedule_day=None,
                         existing_schedules=None, existing_appointments=None,
                         schedule_time_start=None, schedule_time_end=None, doctor=None):
        DoctorScheduleDay = apps.get_model('doctor_profiles.DoctorScheduleDay')
        DateDim = apps.get_model('datesdim.DateDim')
        if force_schedule:
            try:
                schedule_day_object = DoctorScheduleDay.objects.get(id=schedule_day_id)
            except DoctorScheduleDay.DoesNotExist:
                return False, 'Invalid schedule!', status.HTTP_400_BAD_REQUEST
        else:

            today = DateDim.objects.today()

            if schedule_day.date_obj < today.date_obj:
                return False, "You can't schedule an appointment in the past!", status.HTTP_400_BAD_REQUEST

            valid_times = existing_schedules.filter(
                schedule__start_time__minutes_since__lte=schedule_time_start.minutes_since,
                schedule__end_time__minutes_since__gte=schedule_time_end.minutes_since
            )

            if valid_times.count() == 0:
                return False, f"{doctor} does not have a schedule on that time!", status.HTTP_404_NOT_FOUND
            else:
                schedule_day_object = valid_times.first()

            # check available
            collisions = check_collisions(appointments=existing_appointments, schedule_time_start=schedule_time_start,
                                          schedule_time_end=schedule_time_end)

            if collisions.count() > 0:
                return False, "The schedule you want conflicts with an existing schedule!", status.HTTP_409_CONFLICT

        return True, schedule_day_object, None

    def create(self, *args, **kwargs):
        DateDim = apps.get_model('datesdim.DateDim')
        BaseProfile = apps.get_model('profiles.BaseProfile')
        DoctorProfile = apps.get_model('doctor_profiles.DoctorProfile')
        MedicalInstitution = apps.get_model('doctor_profiles.MedicalInstitution')
        MedicalInstitutionDoctor = apps.get_model('doctor_profiles.MedicalInstitutionDoctor')

        patient_id = kwargs.get('patient_id', None)
        force_schedule = kwargs.get('force_schedule', False)
        schedule_choice = kwargs.get('schedule_choice', 'first_available')
        preferred_day = kwargs.get('appointment_day', None)
        appointment_type = kwargs.get('appointment_type', 'checkup')
        medical_institution_id = kwargs.get('medical_institution_id', None)
        doctor_id = kwargs.get('doctor_id')
        preferred_time_start = kwargs.get('preferred_time_start', None)
        preferred_time_end = kwargs.get('preferred_time_end', None)
        schedule_day_id = kwargs.get('schedule_day_id', None)

        if patient_id:
            try:
                patient = BaseProfile.objects.get(id=patient_id)
            except BaseProfile.DoesNotExist:
                return False, "User does not exist", status.HTTP_404_NOT_FOUND
        else:
            return False, "Appointment requires patient", status.HTTP_400_BAD_REQUEST

        if doctor_id:
            try:
                doctor = DoctorProfile.objects.get(id=doctor_id)
            except DoctorProfile.DoesNotExist:
                return False, "Doctor does not exist", status.HTTP_404_NOT_FOUND
        else:
            return False, "Appointment requires doctor", status.HTTP_400_BAD_REQUEST

        if medical_institution_id:
            try:
                medical_institution = MedicalInstitution.objects.get(id=medical_institution_id)
            except MedicalInstitution.DoesNotExist:
                return False, "Medical Institution does not exist", status.HTTP_404_NOT_FOUND
        else:
            return False, "Appointment requires medical institution", status.HTTP_400_BAD_REQUEST

        try:
            mi_connection = MedicalInstitutionDoctor.objects.get(doctor=doctor,
                                                                 medical_institution=medical_institution,
                                                                 is_approved=True)
        except MedicalInstitutionDoctor.DoesNotExist:
            return False, f"{doctor} is not connected to {medical_institution}!", status.HTTP_404_NOT_FOUND

        if preferred_day:
            schedule_day = DateDim.objects.parse_get(preferred_day)
            if not schedule_day:
                return False, "Invalid date given", status.HTTP_400_BAD_REQUEST
        else:
            schedule_day = DateDim.objects.today()

        if force_schedule == 'true':
            existing_schedules = []
            existing_appointments = []
        else:
            schedule_check_result, existing = self.get_existing_schedules(
                doctor=doctor,
                medical_institution=medical_institution,
                schedule_day=schedule_day
            )

            if not schedule_check_result:
                return False, existing, status.HTTP_404_NOT_FOUND
            existing_schedules = existing['existing_schedules']
            existing_appointments = existing['existing_appointments']

        sched_time_result, schedule_times, sched_message = self.get_schedule_times(
            schedule_choice=schedule_choice,
            appointment_type=appointment_type,
            mi_connection=mi_connection,
            start=preferred_time_start,
            end=preferred_time_end,
            existing_schedules=existing_schedules,
            existing_appointments=existing_appointments
        )

        schedule_time_start = schedule_times['schedule_time_start']
        schedule_time_end = schedule_times['schedule_time_end']

        if not sched_time_result:
            return False, f'{schedule_time_start} - {schedule_time_end}: {sched_message}!', status.HTTP_400_BAD_REQUEST

        collision_result, schedule_day_object, collision_status = self.collision_checks(
            force_schedule=force_schedule,
            schedule_day=schedule_day,
            existing_schedules=existing_schedules,
            existing_appointments=existing_appointments,
            schedule_time_start=schedule_time_start,
            schedule_time_end=schedule_time_end,
            doctor=doctor,
            schedule_day_id=schedule_day_id
        )

        if not collision_result:
            return collision_result, schedule_day_object, collision_status

        meta = doctor.get_medical_institution_meta(medical_institution)
        try:
            fee = float(meta['fees'][appointment_type])
        except KeyError:
            fee = 0.0

        if schedule_time_start.minutes_since > schedule_time_end.minutes_since:
            schedule_end = DateDim.objects.parse_get(schedule_day.obj().shift(days=1).format('YYYY-MM-DD'))
        else:
            schedule_end = schedule_day

        appointment = self.model(
            type=appointment_type,
            fee=fee,
            schedule_day=schedule_day,
            schedule_end=schedule_end,
            time_start=schedule_time_start,
            time_end=schedule_time_end,
            patient=patient,
            doctor=doctor,
            medical_institution=medical_institution,
            schedule_day_object=schedule_day_object,
        )

        try:
            appointment.save()
            return True, appointment, status.HTTP_201_CREATED
        except IntegrityError:
            return False, None, status.HTTP_500_INTERNAL_SERVER_ERROR


class DoctorScheduleManager(models.Manager):
    @staticmethod
    def check_collision_days(*, doctor, schedule_days, start_time, end_time):
        existing_schedule_days = doctor.get_schedule_days()

        collisions = []

        for existing in existing_schedule_days:
            if existing.day in schedule_days:
                a, b = existing.schedule.start_time.minutes_since, existing.schedule.end_time.minutes_since
                x, y = start_time.minutes_since, end_time.minutes_since

                if x <= a <= y:
                    collisions.append(
                        {
                            'medical_institution': existing.medical_institution,
                            'day': existing.day,
                            'schedule': existing.schedule,
                            'start_time': existing.schedule.start_time,
                            'end_time': existing.schedule.end_time
                        })


                elif x <= b <= y:
                    collisions.append(
                        {
                            'medical_institution': existing.medical_institution,
                            'day': existing.day,
                            'schedule': existing.schedule,
                            'start_time': existing.schedule.start_time,
                            'end_time': existing.schedule.end_time
                        })

                elif x >= a and y <= b:
                    collisions.append(
                        {
                            'medical_institution': existing.medical_institution,
                            'day': existing.day,
                            'schedule': existing.schedule,
                            'start_time': existing.schedule.start_time,
                            'end_time': existing.schedule.end_time
                        })
        return len(collisions) > 0, collisions

    def valid_times(self, *, start, end):
        TimeDim = apps.get_model('datesdim.TimeDim')
        if not type(start) == TimeDim:
            s = TimeDim.objects.parse(start)
            if not s:
                return False
        else:
            s = start
        if not type(end) == TimeDim:
            e = TimeDim.objects.parse(end)
            if not e:
                return False
        else:
            e = end
        if s.minutes_since > e.minutes_since:
            return False

        if s.minutes_since == e.minutes_since:
            return False

        return True

    def valid_days(self, *, start, end):
        if start.date_obj > end.date_obj:
            return False
        return True

    def create(self, *args, **kwargs):
        DateDim = apps.get_model('datesdim.DateDim')
        doctor = kwargs['doctor']

        start = DateDim.objects.parse_get(kwargs['start_date'])
        end = DateDim.objects.parse_get(kwargs['end_date'])

        if not self.valid_times(start=kwargs['start_time'], end=kwargs['end_time']):
            return False, "Invalid start and end time", []

        if not self.valid_days(start=start, end=end):
            return False, "Invalid start and end dates", []

        schedule_days = DateDim.objects.get_days_between(
            start=start,
            end=end,
            day_filter=kwargs['days']
        )

        has_collisions, collision_days = self.check_collision_days(
            doctor=doctor,
            schedule_days=schedule_days,
            start_time=kwargs['start_time'],
            end_time=kwargs['end_time']
        )
        if has_collisions:
            return False, "Schedule Conflict", collision_days

        return True, "Schedule Created", super(DoctorScheduleManager, self).create(*args, **kwargs)


		
