import base64
import os
import tempfile
from io import BytesIO

import gradio as gr
import requests
from PIL import Image

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")

def put_message_in_chatbot(message, history):
    return "", history + [{"role": "user", "content": message}]

def chat_with_backend(history):
    response = requests.post(BACKEND_URL, json={"history": history})
    response.raise_for_status()
    data = response.json()

    updated_history = data["history"]

    audio_path = None
    if data.get("audio_b64"):
        audio_bytes = base64.b64decode(data["audio_b64"])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            audio_path = f.name

    image_pil = None
    if data.get("image_b64"):
        image_bytes = base64.b64decode(data["image_b64"])
        image_pil = Image.open(BytesIO(image_bytes))

    return updated_history, audio_path, image_pil

with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages", allow_tags=False)
        image_output = gr.Image(height=500, interactive=False)
    with gr.Row():
        audio_output = gr.Audio(autoplay=True)
    with gr.Row():
        message = gr.Textbox(label="Chat with our AI Assistant:")

    message.submit(put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]).then(
        chat_with_backend, inputs=chatbot, outputs=[chatbot, audio_output, image_output]
    )

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=7860)