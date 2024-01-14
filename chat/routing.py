from django.urls import re_path, reverse_lazy
from . import consumers


# URL to route connections to ChatConsumer consumer
websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer),
]

