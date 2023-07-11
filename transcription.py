from whisper_jax import FlaxWhisperPipline
import time 

file = "personal_impact_leadership"
start = time.time()

pipeline = FlaxWhisperPipline("openai/whisper-large-v2")

first_transcription = pipeline(file)
print(first_transcription)
checkpoint1 = time.time()
print("The first transcription takes this many seconds:", checkpoint1-start)
second_transcription = pipeline(file)
print(second_transcription)
checkpoint2 = time.time()
print("The second transcription takes this many seconds:", checkpoint2-checkpoint1)