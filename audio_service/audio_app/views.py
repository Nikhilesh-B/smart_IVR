from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json 
import base64
# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the polls index")

@csrf_exempt
def transcribe_audio(request):
    print("Executed")
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))

        # Extract information from the data
        audio_byte_string = data.get('audio_byte_string')
        print("Here's your audio data", audio_byte_string)
        audio_data = base64.b64decode(audio_byte_string)
        with open('testing123.mp3', 'wb') as audio_file:
            audio_file.write(audio_data)

        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST method is allowed'}, status=405)