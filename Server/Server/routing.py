from django.urls import path

from 示例APP import MessageConsumer

websocket_urlpatterns = [
    path("ws/message/", MessageConsumer.Message.as_asgi()),
]
