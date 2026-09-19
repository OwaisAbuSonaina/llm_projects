from openai import OpenAI
from transformers import pipeline
from pathlib import Path
import torch

from client import client, AUDIO_MODEL

openai = client

audio_filename = str(Path(__file__).parent / "denver_extract.mp3") 

# pipe = pipeline(
#     "automatic-speech-recognition",
#     model="openai/whisper-medium.en",
#     dtype=torch.float16,
#     device='cuda',
#     return_timestamps=True
# )

# result = pipe(audio_filename)
# open_source_transcription = result["text"]
# print(open_source_transcription)


with open(audio_filename, "rb") as audio_file:
    transcription = openai.audio.transcriptions.create(
        model=AUDIO_MODEL,
        file=audio_file,
        response_format="text"
    )

# print(transcription)