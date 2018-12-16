from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def patient_appointment_status_notify(appointment, message, color):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"patient-{appointment.patient.id}-appointments", {
            "type": "notification.alert",
            "event": f"Appointment status changed: {appointment.status}",
            "appointment": f"{appointment}",
            "scope": "global",
            "message": message,
            "color": color
        }
    )