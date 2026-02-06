"""
WebSocket URL routing for logviewer.
"""
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/logs/", consumers.LogViewerConsumer.as_asgi()),
]
