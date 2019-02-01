from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def doctor_notify_new_appointment(appointment):
    channel_layer = get_channel_layer()
    appointment_data = {
            "type": "notification.alert",
            "event": "New appointment",
            "appointment": {
                "id": appointment.id,
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
                },
                "medical_institution": {
                    "name": appointment.medical_institution.name,
                    "type": appointment.medical_institution.type.name,
                    "id": appointment.medical_institution.id,
                    "address": str(appointment.medical_institution.address()['address'])
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
