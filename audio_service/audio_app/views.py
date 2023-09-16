from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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

@csrf_exempt
def voice(request):
    """Respond to incoming phone calls with a 'Hello world' message"""
    if request.METHOD == 'GET':
        # Start our TwiML response
        resp = VoiceResponse()
        # Read a message aloud to the caller
        resp.say("Hello world!")
        return str(resp)

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
    