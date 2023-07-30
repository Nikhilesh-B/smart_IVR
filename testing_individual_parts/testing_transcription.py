#this actually works
import base64
import requests
AUDIOFILE = '/Users/nikhileshbelulkar/Documents/smart_IVR/testing_individual_parts/personal_impact_leadership.mp3'

with open(AUDIOFILE, 'rb') as audio_file:
    audio_data = audio_file.read()

base64_string = base64.b64encode(audio_data).decode('utf-8')
obj = {'audio_byte_string':base64_string}
url = 'http://127.0.0.1:8000/audio_app/transcribe_audio/'
response = requests.post(url=url, json=obj)
print(response)