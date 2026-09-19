import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

LLAMA = "meta-llama/Llama-3.2-3B-Instruct"
AUDIO_MODEL = "gpt-4o-mini-transcribe"

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()