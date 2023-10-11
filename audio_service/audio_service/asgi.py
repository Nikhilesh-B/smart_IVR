"""
ASGI config for audio_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from audio_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_service.settings')

django_asgi_app = get_asgi_application()
django_websocket_asgi_app = AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))

application = ProtocolTypeRouter(
                                {
                                    'http':django_asgi_app,
                                    'websocket':django_websocket_asgi_app
                                    }
                                )
