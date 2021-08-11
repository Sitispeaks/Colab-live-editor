"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()


from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import sharededit.routing


get_asgi_application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns + sharededit.routing.websocket_urlpatterns
        )
    ),
})
# 
# get_asgi_application()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# # django.setup()
# application = get_default_application()


