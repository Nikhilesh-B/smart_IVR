from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt 
import json 
import requests
from audio_app.models import Call_Processor
import socketio
from twilio.twiml.voice_response import VoiceResponse


# Create your views here.
sio = socketio.Client()
form_data = None

def index(request):
    return HttpResponse("Hello world.")


class ServeAudio(View):
    def get(self, request, *args, **kwargs):
        audio_file_path = "/Users/nikhileshbelulkar/Documents/smart_IVR/testing/audio_examples/supportify.mp3"
        return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')

@csrf_exempt
def voice(request):
    """Respond to incoming phone calls with a 'Hello world' message"""
    if request.method == 'POST' or request.method == 'GET':
        # Start our TwiML response
        # Read a message aloud to the caller
        resp = VoiceResponse()
        resp.play("https://6ed0-2600-4040-56c4-9e00-1c3b-216f-8d0e-5b0f.ngrok-free.app/audio_app/supportify.mp3")
        return HttpResponse(str(resp))
    

@sio.on('connect')
def on_connect():
    update_form()
    print("I'm connected!")

def update_form():
    global form_data
    form_data["lock"] = False
    print("update_form")
    print(form_data)
    sio.emit('formSubmit', form_data)

@sio.on('disconnect')
def on_disconnect():
    print("I'm disconnected!")

def generate_fields(text):
    global form_data
    chat = Call_Processor()
    messages = {"role":"user", "content":text}
    res = json.loads(chat.chat_completion_request([messages], chat.functions).content)
    print(res)
    ticket_json = res["choices"][0]["message"]["function_call"]
    form_data = json.loads(ticket_json["arguments"])
    sio.connect("http://localhost:3001")
    sio.disconnect()

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        audio_byte_string = data.get('audio_byte_string')
        filename = data.get('filename')
        #send the audio_byte_string to something on the google cloud for transcritptions

        payload = {'filename':filename, 'audio_byte_string':audio_byte_string}
        url = 'https://supportify-394619.ue.r.appspot.com/transcription/'
        response = requests.post(url=url, json=payload)

        json_out = {'status': 'success'}
        generate_fields(response.text)

        return JsonResponse(json_out)

    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST method is allowed'}, status=405)
    