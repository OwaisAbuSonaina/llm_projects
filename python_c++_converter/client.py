import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

openai_client = OpenAI(api_key=openai_api_key)
gemini_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

OPENAI_MODEL = "gpt-4o" 
GEMENI_MODEL = "gemini-3.1-flash-lite"