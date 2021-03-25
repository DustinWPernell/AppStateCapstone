from django.conf.urls import url

from LifeCounter.consumers import GameConsumer

websocket_urlpatterns = [
    url(r'^ws/<room_code>\w+)/$', GameConsumer.as_asgi()),
]
