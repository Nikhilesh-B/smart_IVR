from django.urls import path
from .views import ServeAudio
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('transcribe_audio/',views.transcribe_audio,name='transcribe_audio'),
    path('voice', views.voice, name='voice'),
    path('supportify.mp3', ServeAudio.as_view(), name='audio_test')
]