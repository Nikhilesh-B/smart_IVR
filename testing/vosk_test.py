import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment, utils
from io import BytesIO

# Path to the model and audio file
model_path = '/Users/nikhileshbelulkar/Documents/smart_IVR/transcription_model/model-en'
audio_file_path = '/Users/nikhileshbelulkar/Documents/smart_IVR/testing/audio_examples/bad_call.mp3'  # replace with your file's path

# Load the model
model = Model(model_path)
channels = utils.mediainfo(audio_file_path)['channels']
sample_rate = utils.mediainfo(audio_file_path)['sample_rate']


# Convert MP3 to WAV using pydub
audio = AudioSegment.from_mp3(audio_file_path)
audio = audio.set_channels(channels).set_frame_rate(sample_rate)
buffer = BytesIO()
audio.export(buffer, format="wav")

# Use BytesIO to "open" the audio data
buffer.seek(0)  # rewind the buffer for reading

# Initialize recognizer
recognizer = KaldiRecognizer(model, sample_rate)

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
