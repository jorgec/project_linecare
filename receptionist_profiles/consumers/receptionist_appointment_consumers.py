import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ReceptionistAppointmentNotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope["user"]

    async def connect(self):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            if doctor:
                await self.accept()
                await self.channel_layer.group_add(f'{doctor.id}-appointments', self.channel_name)
                print(f'channel {self.user.id}-appointments added')

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            if doctor:
                await self.channel_layer.group_discard(f'{doctor.id}-appointments', self.channel_name)
                print(f"Removed {self.channel_name} channel to {doctor.id}-appointments")

    async def notification_alert(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")



