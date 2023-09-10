from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json 
import requests
from audio_app.models import Call_Processor

# Create your views here.

def index(request):
    return HttpResponse("Hello world.")


def generate_fields(text):
    chat = Call_Processor()
    messages = {"role":"user", "content":text}
    res = json.loads(chat.chat_completion_request([messages], chat.functions).content)

    return res["choices"][0]["message"]["function_call"]


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
        json_out.update(generate_fields(response.text))

        return JsonResponse(json_out)

    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST method is allowed'}, status=405)