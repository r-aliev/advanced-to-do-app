from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/comment/(?P<pk>\w+)/$', consumers.CommentConsumer.as_asgi()),
]