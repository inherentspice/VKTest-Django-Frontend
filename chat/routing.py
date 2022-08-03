# from django.urls import re_path
from django.conf.urls import url


from . import consumers

websocket_urlpatterns = [
    url(r'wss/chat/(?P<room_name>[A-Za-z0-9_-]+)/(?P<user_name>\[A-Za-z0-9_-]+)/(?P<role>\[A-Za-z0-9_-]+)/$', consumers.ChatConsumer.as_asgi()),
]
