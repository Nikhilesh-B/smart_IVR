#this actually works
import base64
import requests
import os
import json

AUDIOFILE = os.getcwd() + "/testing/audio_examples/bad_call.mp3"

with open(AUDIOFILE, 'rb') as audio_file:
    audio_data = audio_file.read()

base64_string = base64.b64encode(audio_data).decode('utf-8')
obj = {'filename': 'test_audio.mp3', 'audio_byte_string':base64_string}

url = 'http://127.0.0.1:8000/audio_app/transcribe_audio/'

response = requests.post(url=url, json=obj)
out = json.loads(response.content)["arguments"]

print(json.dumps(json.loads(out), indent=2))