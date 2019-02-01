from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse


def doctor_notify_new_appointment(appointment):
    channel_layer = get_channel_layer()
    schedule_url = reverse("doctor_profile_schedule_detail", kwargs={"medical_institution": appointment.medical_institution.slug}) + f"?date={appointment.schedule_day}&schedule_id={appointment.schedule_day_object.schedule.id}"
    appointment_data = {
        "type": "notification.alert",
        "event": "New appointment",
        "appointment": {
            "id": appointment.id,
            "url": f"{reverse('doctor_profile_patient_appointment_detail')}?appointment={appointment.id}",
            "status": appointment.status,
            "status_display": appointment.get_status_display(),
            "type_display": appointment.get_type_display(),
            "type": appointment.type,
            "queue_number": appointment.queue_number,
            "patient": {
                "name": appointment.patient.get_full_name(),
                "user_id": appointment.patient.user.id,
                "profile_id": appointment.patient.id,
                "photo": appointment.patient.get_profile_photo(),
                "url": reverse('doctor_profile_patient_detail', kwargs={'patient_id': appointment.patient.id})
            },
            "medical_institution": {
                "name": appointment.medical_institution.name,
                "type": appointment.medical_institution.type.name,
                "id": appointment.medical_institution.id,
                "address": str(appointment.medical_institution.address()['address']),
                "url": reverse("doctor_profile_schedule_detail", kwargs={"medical_institution": appointment.medical_institution.slug}) + f"?date={appointment.schedule_day}"
            },
            "schedule": {
                "id": appointment.schedule_day_object.schedule.id,
                "day": str(appointment.schedule_day),
                "day_name": appointment.schedule_day.day_name,
                "month": appointment.schedule_day.month_str(),
                "day_nicename": appointment.schedule_day.nice_name(),
                "name": str(appointment.schedule_day_object.schedule),
                "time_start": appointment.time_start.format_12(),
                "time_end": appointment.time_start.format_12(),
                "url": schedule_url
            }
        },
    }
    appointment.doctor.update_appointment_notifications(appointment_data)
    async_to_sync(channel_layer.group_send)(
        f"{appointment.doctor.id}-appointments", appointment_data
    )


def doctor_notify_update_queue(doctor):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"doctor-queue-{doctor.id}", {
            "type": "queue.update",
            "event": "Queue updated",
            "doctor": f"{doctor}",
        }
    )
