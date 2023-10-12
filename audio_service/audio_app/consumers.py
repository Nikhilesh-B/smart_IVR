import json
import vosk, base64, audioop
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))

class TranscriptionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CL = '\x1b[0K'
        self.BS = '\x08'
        self.model_path = '/Users/nikhileshbelulkar/Documents/smart_IVR/transcription_model/model-en'
        self.model = vosk.Model(self.model_path)

    async def connect(self):
        print("We are connecting")
        await self.accept()

    async def disconnect(self, close_code):
        print("hello")
        pass

    async def recieve(self, audio):
        """Receive and transcribe audio stream."""
        rec = vosk.KaldiRecognizer(self.model, 16000)
        while True:
            packet = json.loads(audio)
            if packet['event'] == 'start':
                print('Streaming is starting')
            elif packet['event'] == 'stop':
                print('\nStreaming has stopped')
            elif packet['event'] == 'media':
                audio = base64.b64decode(packet['media']['payload'])
                audio = audioop.ulaw2lin(audio, 2)
                audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
                if rec.AcceptWaveform(audio):
                    r = json.loads(rec.Result())
                    print(self.CL + r['text'] + ' ', end='', flush=True)
                else:
                    r = json.loads(rec.PartialResult())
                    print(self.CL + r['partial'] + self.BS * len(r['partial']), end='', flush=True)
            await self.close()
            