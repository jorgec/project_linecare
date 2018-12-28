from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from doctor_profiles.consumers.doctor_appointment_consumers import DoctorAppointmentNotificationConsumer
from profiles.consumers.patient_appointment_consumers import PatientAppointmentNotificationConsumer
from receptionist_profiles.consumers import ReceptionistAppointmentNotificationConsumer

application = ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(
        URLRouter([
            path("notifications/receptionist/appointments/", ReceptionistAppointmentNotificationConsumer),
            path('notifications/patient/appointment/status/', PatientAppointmentNotificationConsumer),
            path('notifications/doctor/queue/status_update/', DoctorAppointmentNotificationConsumer)
        ])
    )
})
