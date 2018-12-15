import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AppointmentNotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope["user"]

    async def connect(self):
        if self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(f'{self.user.id}-appointments', self.channel_name)
            print(f'channel {self.user.id}-appointments added')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f'{self.user.id}-appointments', self.channel_name)
        print(f"Removed {self.channel_name} channel to {self.user.id}-appointments")

    async def notification_alert(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")



