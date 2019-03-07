import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ReceptionistAppointmentNotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope["user"]

    async def connect(self):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            receptionist = self.user.receptionist_profile()
            if doctor:
                await self.accept()
                await self.channel_layer.group_add(f'doctor-{doctor.id}-appointments', self.channel_name)
            if receptionist:
                await self.accept()
                await self.channel_layer.group_add(f'receptionist-{receptionist.id}-appointments', self.channel_name)

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            receptionist = self.user.receptionist_profile()
            if doctor:
                await self.channel_layer.group_discard(f'doctor-{doctor.id}-appointments', self.channel_name)
            if receptionist:
                await self.channel_layer.group_discard(f'receptionist-{receptionist.id}-appointments', self.channel_name)

    async def notification_alert(self, event):
        await self.send_json(event)



