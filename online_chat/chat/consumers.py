import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from chat.models import ChatMessage3, UserMessege3, User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = ChatMessage3.objects.get(id=self.room_name)
        self.update_online_status(self.user, True)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        
        message = UserMessege3.objects.filter(chat_room=self.room).order_by("-id")
        for mes in reversed(message):
            self.send(text_data=json.dumps({
                "message": mes.text,
                'user': mes.user.username,
                "datetime": json.dumps(mes.created, indent=4, sort_keys=True, default=str)
            }))

    def disconnect(self, close_code):
        # Leave room group
        self.update_online_status(self.user, False)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()
        datetime = now.isoformat()
        UserMessege3.objects.create(chat_room=self.room, user=self.user, text=message)
        chat_update = ChatMessage3.objects.get(id=self.room_name)
        chat_update.updated = now
        chat_update.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message,
                                   "user": self.user.username,
                                   "datetime": datetime}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        datetime = event["datetime"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "user": user, "datetime": datetime}))
        
    def update_online_status(self, user, status):
        # Broadcast online status change to room group
        get_user = User.objects.get(id=user.id)
        get_user.online = status
        get_user.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'user.online_status',
                'user': user.username,
                'status': status,
                'last_online': json.dumps(get_user.last_online, indent=4, sort_keys=True, default=str)
            }
        )
        
    def user_online_status(self, event):
        user = event['user']
        status = event['status']
        last_online = event['last_online']
        # Send online status change message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'user.online_status',
            'user': user,
            'status': status,
            'last_online': last_online
        }))