from django.urls import re_path
from . import consumers

websocket_urlpatterns = [re_path("/ws/audio_app/audio_transcription/$", consumers.TranscriptionConsumer.as_asgi()),
                         re_path(r"ws/audio_app/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi())]