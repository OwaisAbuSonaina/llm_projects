import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not (api_key and api_key.startswith("sk-proj-") and len(api_key) > 10):
    print("Warning: There might be a problem with your API key", file=sys.stderr)

DEFAULT_MODEL = "gpt-5-nano"

client = OpenAI()