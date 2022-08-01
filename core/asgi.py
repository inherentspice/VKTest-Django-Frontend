import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# application = get_default_application()
application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': URLRouter(
            chat.routing.websocket_urlpatterns
        ),
})
