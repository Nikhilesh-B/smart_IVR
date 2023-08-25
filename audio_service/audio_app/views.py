from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json 
import requests

# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the polls index")


def generate_important_fields(text):
    pass


@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        audio_byte_string = data.get('audio_byte_string')
        #send the audio_byte_string to something on the google cloud for transcritptions

        payload = {'audio_byte_string':audio_byte_string}
        url = 'http://127.0.0.1:5000/transcription'
        response = requests.post(url=url, json=payload)
        print(response)

        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST method is allowed'}, status=405)