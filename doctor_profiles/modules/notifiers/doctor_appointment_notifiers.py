from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def doctor_notify_new_appointment(appointment):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{appointment.doctor.id}-appointments", {
            "type": "notification.alert",
            "event": "New appointment",
            "appointment": f"{appointment}"
        }
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