from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .call_processor import Call_Processor
import socketio
from twilio.twiml.voice_response import VoiceResponse, Start
import firebase_admin
from firebase_admin import credentials

# Create your views here.
sio = socketio.Client()
form_data = None


def index(request):
    return render(request, "audio_app/index.html")


def room(request, room_name):
    return render(request, "audio_app/room.html", {"room_name": room_name})


class ServeAudio(View):
    def get(self, request, *args, **kwargs):
        audio_file_path = "/Users/nikhileshbelulkar/Documents/smart_IVR/testing/audio_examples/supportify.mp3"
        return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')


@csrf_exempt
def voice(request):
    """Respond to incoming phone calls with a 'Hello world' message"""
    if request.method == 'POST':
        # Start our TwiML response
        # Read a message aloud to the caller
        resp = VoiceResponse()
        start = Start()
        print(f'wss://{request.get_host()}/audio_transcription')
        # this request isn't working
        start.stream(
            url=f'wss://{request.get_host()}/audio_app/audio_transcription')
        resp.append(start)
        resp.say('Please leave a message')
        resp.pause(length=3)
        print(f'Incoming call from {request.POST["From"]}')
        return HttpResponse(content=str(resp), content_type='text/xml', status=200)


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

def get_user_uid(request):
    cred = credentials.Certificate("../../../service-account.json")
    firebase_admin.initialize_app(cred)

    from firebase_admin import auth
    if request.method == 'GET':
        email = request.GET.get('email')
        user = auth.get_user_by_email(email)
        uid = user.uid
        return JsonResponse({'uid': uid})


def generate_fields(text):
    global form_data
    chat = Call_Processor()
    messages = {"role": "user", "content": text}
    res = json.loads(chat.chat_completion_request(
        [messages], chat.functions).content)
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
        # send the audio_byte_string to something on the google cloud for transcritptions

        payload = {'filename': filename,
                   'audio_byte_string': audio_byte_string}
        url = 'https://supportify-394619.ue.r.appspot.com/transcription/'
        response = requests.post(url=url, json=payload)

        json_out = {'status': 'success'}
        generate_fields(response.text)

        return JsonResponse(json_out)

    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST method is allowed'}, status=405)
