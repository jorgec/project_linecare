from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from receptionist_profiles.consumers import AppointmentNotificationConsumer

application = ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(
        URLRouter([
            path("appointment-notifications/", AppointmentNotificationConsumer)
        ])
    )
})
