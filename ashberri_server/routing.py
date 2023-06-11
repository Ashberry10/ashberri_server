from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import consumers

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(consumers.websocket_urlpatterns),
})
