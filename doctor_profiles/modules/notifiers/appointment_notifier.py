from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_new_appointment(appointment):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{appointment.doctor.user.id}-appointments", {
            "type": "notification.alert",
            "event": "New appointment",
            "appointment": f"{appointment}"
        }
    )