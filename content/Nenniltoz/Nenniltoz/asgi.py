"""
ASGI config for Nenniltoz project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import LifeCounter.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nenniltoz.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
    URLRouter(
      LifeCounter.routing.websocket_urlpatterns
    )
  ),
})