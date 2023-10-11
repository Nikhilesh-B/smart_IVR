import json
import vosk, base64, audioop
from channels.generic.websocket import AsyncWebsocketConsumer

class TranscriptionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CL = '\x1b[0K'
        self.BS = '\x08'
        self.model = vosk.Model('model-en')

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
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
            