from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models as models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from django.apps import apps

from doctor_profiles.models.managers.doctor_schedule_manager import DoctorScheduleManager


class DoctorSchedule(models.Model):
    """
    Doctor Schedule instance
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_regular = models.BooleanField(default=True)

    """
    Days
    """
    days = ArrayField(models.CharField(max_length=15, null=True, blank=True), null=True, blank=True)

    """
    Admin
    """
    is_approved = models.BooleanField(default=True)

    """
    Relationship Fields
    """
    start_time = models.ForeignKey('datesdim.TimeDim', related_name='schedule_start_time', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    end_time = models.ForeignKey('datesdim.TimeDim', related_name='schedule_end_time', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    start_date = models.ForeignKey('datesdim.DateDim', related_name='schedule_start_date', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    end_date = models.ForeignKey('datesdim.DateDim', related_name='schedule_end_date', null=True, blank=True,
                                 on_delete=models.SET_NULL)

    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='doctor_schedules',
                               on_delete=models.CASCADE)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution', related_name='mi_doctor_schedules',
                                            on_delete=models.CASCADE)
    created_by = models.ForeignKey('accounts.Account', related_name='schedule_creator', on_delete=models.SET_NULL,
                                   null=True, blank=True)

    objects = DoctorScheduleManager()

    def __str__(self):
        if len(self.days) > 0:
            days = ", ".join(self.days)
        else:
            days = "No days scheduled"
        return f'{self.doctor} schedule in {self.medical_institution} ({days})'

    class Meta:
        ordering = ('start_date',)

    def split_days(self):
        return ", ".join(self.days)


class DoctorScheduleDay(models.Model):
    """
    Doctor Schedule Day instance
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    day = models.ForeignKey('datesdim.DateDim', related_name='schedule_days', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='doctor_schedule_days',
                               on_delete=models.CASCADE)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution',
                                            related_name='mi_doctor_schedule_days',
                                            on_delete=models.CASCADE)
    schedule = models.ForeignKey(DoctorSchedule, related_name='schedule_on_days', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day} - {self.schedule}'


class PatientAppointment(models.Model):
    """
    Scheduled appointments
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship fields
    schedule_day = models.ForeignKey('datesdim.DateDim', on_delete=models.SET_NULL,
                                     related_name='day_scheduled_patients',
                                     null=True, blank=True)
    time_start = models.ForeignKey('datesdim.TimeDim', on_delete=models.SET_NULL,
                                   related_name='time_start_scheduled_patients',
                                   null=True, blank=True)
    time_end = models.ForeignKey('datesdim.TimeDim', on_delete=models.SET_NULL,
                                 related_name='time_end_scheduled_patients',
                                 null=True, blank=True)
    patient = models.ForeignKey('profiles.BaseProfile', on_delete=models.SET_NULL,
                                related_name='patient_scheduled_appointments',
                                null=True, blank=True)
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL,
                               related_name='doctor_scheduled_appointments',
                               null=True, blank=True)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution', on_delete=models.SET_NULL,
                                            related_name='medical_institution_scheduled_appointments',
                                            null=True, blank=True)

    class Meta:
        ordering = ('-schedule_day',)
        unique_together = ('patient', 'doctor', 'medical_institution', 'schedule_day', 'time_start', 'time_end')

    def __str__(self):
        return f'{self.schedule_day} - {self.patient}'


@receiver(post_save, sender=DoctorSchedule)
def populate_schedule_days(sender, instance=None, created=False, **kwargs):
    if created and instance:
        if instance.is_regular:
            DateDim = apps.get_model('datesdim.DateDim')
            date_range = DateDim.objects.get_days_between(
                start=instance.start_date,
                end=instance.end_date,
                day_filter=instance.days
            )

            for day in date_range:
                DoctorScheduleDay.objects.create(
                    day=day,
                    doctor=instance.doctor,
                    medical_institution=instance.medical_institution,
                    schedule=instance
                )
