from django.urls import re_path
import exam.consumers

websocket_urlpatterns=[
    re_path(r'ws/exam/stream/videoStream/(?P<v_name>\w+)/$', exam.consumers.VideoConsumer.as_asgi())
]