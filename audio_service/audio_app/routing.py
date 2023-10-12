from django.urls import re_path
from . import consumers

websocket_urlpatterns = [re_path("/ws/audio_transcription/$", consumers.TranscriptionConsumer.as_asgi())]