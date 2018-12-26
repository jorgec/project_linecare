from django.core.exceptions import ObjectDoesNotExist
from django.db import models as models
from django.apps import apps
from django.db.models import Q

from doctor_profiles.constants import QUEUE_DONE_CODES, QUEUE_STATUS_MESSAGES
from profiles.notifiers.patient_appointment_notifiers import patient_appointment_status_notify


class PatientAppointmentQuerySet(models.QuerySet):
    def prior_visits(self, *, doctor, patient):
        return self.filter(
            doctor=doctor,
            patient=patient,
        )


class PatientAppointmentManager(models.Manager):
    def get_queryset(self):
        return PatientAppointmentQuerySet(self.model, using=self._db)

    def prior_visits(self, *, doctor, patient):
        return self.get_queryset().prior_visits(
            doctor=doctor,
            patient=patient,
        )

    def update_status(self, *, id, status):
        appointment = self.get(id=id)
        appointment.status = status
        appointment.save()
        patient_appointment_status_notify(appointment,
                                          QUEUE_STATUS_MESSAGES[status]['message'],
                                          QUEUE_STATUS_MESSAGES[status]['color'])


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

        if not self.valid_times(start=kwargs['start_time'], end=kwargs['end_time']):
            return False, "Invalid start and end time", []

        schedule_days = DateDim.objects.get_days_between(
            start=DateDim.objects.parse_get(kwargs['start_date']),
            end=DateDim.objects.parse_get(kwargs['end_date']),
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
    TimeDim = apps.get_model('datesdim.TimeDim')
    for schedule in schedules:
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
    )
