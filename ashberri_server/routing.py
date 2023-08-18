from django.urls import re_path
from django.core.asgi import get_asgi_application  # Add this import for deploy
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import consumers

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(consumers.websocket_urlpatterns),
})
