import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DoctorAppointmentNotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope["user"]

    async def connect(self):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            if doctor:

                await self.accept()
                medical_institutions = doctor.get_medical_institutions()
                for mi in medical_institutions:
                    await self.channel_layer.group_add(
                        f'doctor-queue-{doctor.id}-{mi.id}', self.channel_name
                    )

    async def disconnect(self, code):
        if self.user.is_authenticated:
            doctor = self.user.doctor_profile()
            if doctor:
                medical_institutions = await doctor.get_medical_institutions()
                for mi in medical_institutions:
                    await self.channel_layer.group_discard(f'doctor-queue-{doctor.id}-{mi.id}', self.channel_name)

    async def queue_update(self, event):
        await self.send_json(event)
