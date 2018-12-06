from django.core.exceptions import ObjectDoesNotExist
from django.db import models as models
from django.apps import apps


class DoctorScheduleManager(models.Manager):
    def check_collision_days(self, *, doctor, schedule_days, start_time, end_time):
        existing_schedule_days = doctor.get_schedule_days()

        collisions = []
        has_collisions = False

        for existing in existing_schedule_days:
            if existing.day in schedule_days:
                candidate = schedule_days.get(id=existing.day.id)
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

        return has_collisions, collisions

    def create(self, *args, **kwargs):
        Doctor = apps.get_model('doctor_profiles.DoctorProfile')
        DateDim = apps.get_model('datesdim.DateDim')
        try:
            doctor = Doctor.objects.get(pk=kwargs['doctor_id'])
        except Doctor.DoesNotExist:
            raise ObjectDoesNotExist("Doctor does not exist")

        schedule_days = DateDim.objects.get_days_between(
            start=kwargs['start_date'],
            end=kwargs['end_date'],
            day_filter=['days']
        )

        has_collision, collision_days = self.check_collision_days(doctor=doctor, schedule_days=schedule_days,
                                                                  start_time=kwargs['start_time'],
                                                                  end_time=kwargs['end_time'])
