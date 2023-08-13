"""
ASGI config for ashberri_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import application as websocket_application  # Import the websocket application from your routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ashberri_server.settings')

# HTTP application
http_application = get_asgi_application()

# WebSocket application
application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": websocket_application,
})
