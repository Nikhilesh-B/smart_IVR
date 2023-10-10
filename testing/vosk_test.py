import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment, utils
from io import BytesIO

# Path to the model and audio file
model_path = '/Users/nikhileshbelulkar/Documents/smart_IVR/transcription_model/model-en'
audio_file_path = '/Users/nikhileshbelulkar/Documents/smart_IVR/testing/audio_examples/supportify.mp3'


# Load the model
model = Model(model_path)


# Convert MP3 to WAV using pydub
audio = AudioSegment.from_mp3(audio_file_path)
audio = audio.set_channels(1).set_frame_rate(16000)
buffer = BytesIO()
audio.export(buffer, format="wav")


# Use BytesIO to "open" the audio data
buffer.seek(0)  # rewind the buffer for reading

# Initialize recognizer
recognizer = KaldiRecognizer(model, 16000)

# Read audio in chunks and feed to recognizer
while True:
    data = buffer.read(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print(result['text'])

# Print the final result
result = json.loads(recognizer.FinalResult())
print(result['text'])
