from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('transcribe_audio/',views.transcribe_audio,name='transcribe_audio'),
    path('voice', views.voice, name='voice')
]