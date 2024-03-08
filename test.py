import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

import json

project_id = "smiling-spider-416615"
location = "europe-west1"
vertexai.init(project=project_id, location=location)
model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
        print( chunk.text)
    return ""

get_chat_response(chat, "Hola, como estás?")