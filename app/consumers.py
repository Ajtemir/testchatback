import datetime
import json
import django
django.setup()
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from app.models import Message


class TextRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender = text_data_json['sender']
        receiver = self.room_group_name.split('_')[1]
        await self.create_new_comment(sender, receiver, text)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        # Receive message from room group
        text = event['message']
        sender = event['sender']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'text': text,
            'sender': sender
        }))

    @database_sync_to_async
    def create_new_comment(self, sender, receiver, text):
        print(sender, receiver, text)
        user_from = User.objects.filter(username=sender).first()
        user_to = User.objects.filter(username=receiver).first()
        message = Message.objects.create(
            message=text,
            user_from=user_from,
            user_to=user_to,
            timestamp=datetime.datetime.now()
        )
        return message
