from django.core.asgi import get_asgi_application
import os
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': URLRouter(
            chat.routing.websocket_urlpatterns
        ),
})
