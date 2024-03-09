import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

from threading import Thread

class CustomThread(Thread):
    # constructor
    def __init__(self,promptTexts):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
        self.texts = promptTexts
 
    # function executed in a new thread
    def run(self):
        # store data in an instance variable
        self.value = get_Summary(self.texts)

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
    return " ".join(text_response)

def get_Summary(texts: list)->str:
    prompt = "Cada uno de los siguientes números es un artículo. Es decir el 0: es el artículo 0, el 1: es el artículo 1 y así sucesivamente. Quiero un resumen claramente separado de cada uno de los artículos de unas 8 líneas como mucho por cada uno de ellos conteniendo los puntos más importantes"
    for index, text in enumerate(texts):
        print(f"{index}: {text}")
        prompt+= f'\n {index}.  {text}'
    return get_chat_response(chat, prompt)