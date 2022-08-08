import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room, Message, User
import requests


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.username = None
        self.role = None
        self.question = None
        self.results = None


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.username = self.scope['url_route']['kwargs']['user_name']
        self.role = self.scope['url_route']['kwargs']['role']
        User.objects.filter(username=self.username).delete()
        self.user, create = User.objects.get_or_create(username=self.username)
        self.question = self.room.question
        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # # send the user list to the newly joined user
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        self.room.online.remove(self.user)
        User.objects.filter(username=self.username).delete()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if int(self.role) == 42 or int(self.role) == 19:
            self.results = True
        else:
            self.results = False

        if self.results==False:
            if int(self.role) % 2 == 0:
                url = "https://vktest-kr575za6oa-uw.a.run.app/response?"
                payload = {'question': self.question}
                message = requests.get(url, params=payload).json()['response']
                print(message)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': self.username,
                    'message': message,
                }
            )
        else:
            if int(self.role) % 2 == 0:
                message = 'is an AI'
            else:
                message = 'is Human'

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': self.username,
                    'message': message,
                }
            )
        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))
