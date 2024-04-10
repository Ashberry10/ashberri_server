# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))





from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Perform any necessary connection setup
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the chat room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Perform any necessary cleanup when the WebSocket closes

        # Leave the chat room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Process incoming WebSocket messages
        data = json.loads(text_data)
        message = data.get('message')
        sender = data.get('sender')
        recipient = data.get('recipient')

        # Send the message to the recipient
        await self.send_message_to_recipient(sender, recipient, message)

    async def send_message_to_recipient(self, sender, recipient, message):
        # Send the chat message to the recipient's WebSocket

        # Construct the channel name for the recipient
        recipient_channel = f'user_{recipient}'

        # Send the message to the recipient's channel
        await self.channel_layer.send(
            recipient_channel,
            {
                'type': 'chat.message',
                'sender': sender,
                'message': message
            }
        )

    async def chat_message(self, event):
        # Send the chat message to the WebSocket

        sender = event['sender']
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))
