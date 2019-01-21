import arrow
from django.apps import apps
from django.conf import settings
from django.db import models as models
from django.db.models import Q

from doctor_profiles.constants import QUEUE_STATUS_MESSAGES, QUEUE_CANCELLED_CODES, QUEUE_INACTIVE
from profiles.notifiers.patient_appointment_notifiers import patient_appointment_status_notify


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
        patient_appointment_status_notify(appointment,
                                          QUEUE_STATUS_MESSAGES[status]['message'],
                                          QUEUE_STATUS_MESSAGES[status]['color'])


    def create(self, *args, **kwargs):
        DateDim = apps.get_model('datesdim.DateDim')

        obj = super(PatientAppointmentManager, self).create(*args, **kwargs)
        meta = obj.doctor.get_medical_institution_meta(obj.medical_institution)
        try:
            fee = float(meta['fees'][obj.type])
        except KeyError:
            fee = 0.0
        obj.fee = fee

        if obj.time_start.minutes_since > obj.time_end.minutes_since:
            obj.schedule_end = DateDim.objects.parse_get(obj.schedule_day.obj().shift(days=1).format('YYYY-MM-DD'))
        else:
            obj.schedule_end = obj.schedule_day

        obj.save()
        return True, obj


class DoctorScheduleManager(models.Manager):
    @staticmethod
    def check_collision_days(*, doctor, schedule_days, start_time, end_time):
        existing_schedule_days = doctor.get_schedule_days()

        collisions = []

        for existing in existing_schedule_days:
            if existing.day in schedule_days:
                """
                TODO:
                check times, given:
                -- a, b -> existing times
                -- x, y -> candidate times
                -- collisions:
                ---- [x <= a, y >= a]
                ---- [x <= b, y >= b]
                ---- [x >= a, y <= b]
                """
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

    def create(self, *args, **kwargs):
        DateDim = apps.get_model('datesdim.DateDim')
        doctor = kwargs['doctor']

        start = DateDim.objects.parse_get(kwargs['start_date'])
        end = DateDim.objects.parse_get(kwargs['end_date'])

        if not self.valid_times(start=kwargs['start_time'], end=kwargs['end_time']):
            return False, "Invalid start and end time", []

        schedule_days = DateDim.objects.get_days_between(
            start=start,
            end=end,
            day_filter=kwargs['days']
        )

        has_collisions, collision_days = self.check_collision_days(doctor=doctor, schedule_days=schedule_days,
                                                                   start_time=kwargs['start_time'],
                                                                   end_time=kwargs['end_time'])
        if has_collisions:
            return False, "Schedule Conflict", collision_days

        return True, "Schedule Created", super(DoctorScheduleManager, self).create(*args, **kwargs)


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
