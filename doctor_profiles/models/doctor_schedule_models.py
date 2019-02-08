from _socket import gaierror

import arrow
from django.apps import apps
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models as models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from doctor_profiles.constants import QUEUE_STATUS_CODES, APPOINTMENT_TYPES
from doctor_profiles.models.managers.doctor_schedule_manager import (
    DoctorScheduleManager,
    PatientAppointmentManager,
)
from doctor_profiles.modules.notifiers.doctor_appointment_notifiers import (
    doctor_notify_update_queue,
    doctor_notify_new_appointment,
)


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
    days = ArrayField(
        models.CharField(max_length=15, null=True, blank=True), null=True, blank=True
    )

    """
    Admin
    """
    is_approved = models.BooleanField(default=True)

    """
    Relationship Fields
    """
    start_time = models.ForeignKey(
        "datesdim.TimeDim",
        related_name="schedule_start_time",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    end_time = models.ForeignKey(
        "datesdim.TimeDim",
        related_name="schedule_end_time",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    start_date = models.ForeignKey(
        "datesdim.DateDim",
        related_name="schedule_start_date",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    end_date = models.ForeignKey(
        "datesdim.DateDim",
        related_name="schedule_end_date",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    doctor = models.ForeignKey(
        "doctor_profiles.DoctorProfile",
        related_name="doctor_schedules",
        on_delete=models.CASCADE,
    )
    medical_institution = models.ForeignKey(
        "doctor_profiles.MedicalInstitution",
        related_name="mi_doctor_schedules",
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        "accounts.Account",
        related_name="schedule_creator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = DoctorScheduleManager()

    def __str__(self):
        if len(self.days) > 0:
            days = ", ".join(self.days)
        else:
            days = "No days scheduled"
        return f"{self.doctor} schedule in {self.medical_institution} ({days})"

    class Meta:
        ordering = ("start_date",)

    def split_days(self):
        return ", ".join(self.days)

    def get_schedule_days(self):
        return self.schedule_on_days.all()


class DoctorScheduleDay(models.Model):
    """
    Doctor Schedule Day instance
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    doctor_is_in = models.BooleanField(default=False)
    doctor_stepped_out = models.BooleanField(default=False)

    day = models.ForeignKey(
        "datesdim.DateDim", related_name="schedule_days", on_delete=models.CASCADE
    )
    actual_start_time = models.ForeignKey(
        "datesdim.TimeDim",
        related_name="actual_schedule_start_time",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    actual_end_time = models.ForeignKey(
        "datesdim.TimeDim",
        related_name="actual_schedule_end_time",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    doctor = models.ForeignKey(
        "doctor_profiles.DoctorProfile",
        related_name="doctor_schedule_days",
        on_delete=models.CASCADE,
    )
    medical_institution = models.ForeignKey(
        "doctor_profiles.MedicalInstitution",
        related_name="mi_doctor_schedule_days",
        on_delete=models.CASCADE,
    )
    schedule = models.ForeignKey(
        DoctorSchedule, related_name="schedule_on_days", on_delete=models.CASCADE
    )

    # objects = DoctorScheduleDayManager()

    def __str__(self):
        return f"{self.day} - {self.schedule}"

    def short(self):
        return f"{self.medical_institution}"

    def get_appointments(self):
        return self.day_schedule_object_patients.all()


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
    status = models.CharField(
        choices=QUEUE_STATUS_CODES, max_length=50, default="pending"
    )
    type = models.CharField(choices=APPOINTMENT_TYPES, max_length=50, default="checkup")
    queue_number = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Relationship fields
    schedule_day = models.ForeignKey(
        "datesdim.DateDim",
        on_delete=models.SET_NULL,
        related_name="day_scheduled_patients",
        null=True,
        blank=True,
    )
    schedule_end = models.ForeignKey(
        "datesdim.DateDim",
        on_delete=models.SET_NULL,
        related_name="day_schedule_end_patients",
        null=True,
        blank=True,
    )
    time_start = models.ForeignKey(
        "datesdim.TimeDim",
        on_delete=models.SET_NULL,
        related_name="time_start_scheduled_patients",
        null=True,
        blank=True,
    )
    time_end = models.ForeignKey(
        "datesdim.TimeDim",
        on_delete=models.SET_NULL,
        related_name="time_end_scheduled_patients",
        null=True,
        blank=True,
    )
    patient = models.ForeignKey(
        "profiles.BaseProfile",
        on_delete=models.SET_NULL,
        related_name="patient_scheduled_appointments",
        null=True,
        blank=True,
    )
    doctor = models.ForeignKey(
        "doctor_profiles.DoctorProfile",
        on_delete=models.SET_NULL,
        related_name="doctor_scheduled_appointments",
        null=True,
        blank=True,
    )
    medical_institution = models.ForeignKey(
        "doctor_profiles.MedicalInstitution",
        on_delete=models.SET_NULL,
        related_name="medical_institution_scheduled_appointments",
        null=True,
        blank=True,
    )
    schedule_day_object = models.ForeignKey(
        DoctorScheduleDay,
        on_delete=models.SET_NULL,
        related_name="day_schedule_object_patients",
        null=True,
        blank=True,
    )

    objects = PatientAppointmentManager()

    class Meta:
        ordering = ("-schedule_day", "time_start__minutes_since")
        unique_together = (
            "patient",
            "doctor",
            "medical_institution",
            "schedule_day",
            "time_start",
            "time_end",
            "status",
            "created",
        )

    def __str__(self):
        return f"{self.schedule_day} - {self.time_start.format_12()}"

    def nice_name(self):
        return f"{self.schedule_day.nice_name()} {self.time_start.format_12()}"

    def get_symptoms(self):
        return self.appointment_checkup.checkup_symptoms.filter(is_deleted=False)

    def get_deleted_symptoms(self):
        return self.appointment_checkup.checkup_symptoms.filter(is_deleted=True)

    def get_findings(self):
        return self.appointment_checkup.checkup_findings.filter(is_deleted=False)

    def get_deleted_findings(self):
        return self.appointment_checkup.checkup_findings.filter(is_deleted=True)

    def get_diagnoses(self):
        return self.appointment_checkup.checkup_diagnoses.filter(is_deleted=False)

    def get_deleted_diagnoses(self):
        return self.appointment_checkup.checkup_diagnoses.filter(is_deleted=True)

    def get_prescriptions(self):
        return self.appointment_checkup.checkup_prescriptions.filter(is_deleted=False)

    def get_deleted_prescriptions(self):
        return self.appointment_checkup.checkup_prescriptions.filter(is_deleted=True)

    def get_lab_tests(self):
        return self.appointment_checkup.checkup_tests.filter(is_approved=True)

    def get_deleted_lab_tests(self):
        return self.appointment_checkup.checkup_tests.filter(is_approved=False)

    def get_notes(self):
        return self.appointment_checkup.checkup_notes.all()

    def shift_time(self, time_start=None, save=True):
        TimeDim = apps.get_model("datesdim.TimeDim")
        DateDim = apps.get_model("datesdim.DateDim")

        if not time_start:
            new_time_start = TimeDim.objects.parse(
                arrow.utcnow().to(settings.TIME_ZONE).datetime
            )
        else:
            new_time_start = time_start

        difference = new_time_start.minutes_since - self.time_start.minutes_since

        self.time_start = new_time_start

        try:
            self.time_end = TimeDim.objects.get(
                minutes_since=self.time_end.minutes_since + difference
            )
        except TimeDim.DoesNotExist:
            # move to next day
            self.schedule_end = DateDim.objects.parse_get(
                self.schedule_day.obj().shift(days=1).format("YYYY-MM-DD")
            )

            spillover = difference - (1440 - self.time_end.minutes_since)
            new_time_end = TimeDim.objects.get(minutes_since=spillover)
            self.time_end = new_time_end

        if save:
            self.save()
        else:
            return self


@receiver(post_save, sender=PatientAppointment)
def add_new_to_patient_connection(sender, instance, created=False, **kwargs):
    if created and instance:
        try:
            doctor_notify_new_appointment(instance)
        except gaierror:
            pass
        PatientConnection = apps.get_model("doctor_profiles.PatientConnection")
        try:
            PatientConnection.objects.create(
                patient=instance.patient,
                doctor=instance.doctor,
                metadata={"initial_day": str(instance.schedule_day)},
            )
        except IntegrityError:
            pass


@receiver(post_save, sender=PatientAppointment)
def create_checkup_record(sender, instance, created=False, **kwargs):
    if created:
        CheckupRecord = apps.get_model("doctor_profiles.PatientCheckupRecord")
        CheckupRecordAccess = apps.get_model(
            "doctor_profiles.PatientCheckupRecordAccess"
        )
        try:
            record = CheckupRecord.objects.create(appointment=instance)
        except IntegrityError:
            record = CheckupRecord.objects.get(appointment=instance)

        try:
            access = CheckupRecordAccess.objects.create(
                checkup=record, doctor=instance.doctor
            )
        except IntegrityError:
            pass


@receiver(post_save, sender=PatientAppointment)
def notify_queue_consumers(sender, instance, created=False, **kwargs):
    if instance:
        try:
            doctor_notify_update_queue(instance.doctor)
        except gaierror:
            pass


@receiver(post_save, sender=DoctorSchedule)
def populate_schedule_days(sender, instance=None, created=False, **kwargs):
    if created and instance:
        DateDim = apps.get_model("datesdim.DateDim")
        date_range = DateDim.objects.get_days_between(
            start=instance.start_date, end=instance.end_date, day_filter=instance.days
        )

        for day in date_range:
            DoctorScheduleDay.objects.create(
                day=day,
                doctor=instance.doctor,
                medical_institution=instance.medical_institution,
                schedule=instance,
            )
