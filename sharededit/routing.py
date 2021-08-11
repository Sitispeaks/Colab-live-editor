from django.urls import re_path

from .consumers import SharedEditConsumer

websocket_urlpatterns = [
    re_path(r'ws/sharededit/(?P<room_name>\w+)/$', SharedEditConsumer.as_asgi()),
]
