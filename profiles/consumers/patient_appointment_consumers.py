import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PatientAppointmentNotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope["user"]

    async def connect(self):
        if self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(f'patient-{self.user.base_profile().id}-appointments', self.channel_name)
            print(f'channel patient-{self.user.base_profile().id}-appointments added')

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(f'patient-{self.user.base_profile().id}-appointments', self.channel_name)
            print(f"Removed {self.channel_name} channel to patient-{self.user.base_profile().id}-appointments")

    async def notification_alert(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")





