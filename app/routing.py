from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path, path
from app.consumers import TextRoomConsumer

websocket_urlpatterns = [
    re_path(r'^ws/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})
