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
    response = chat.send_message(prompt)
    return response.candidates[0].content.parts[0]._raw_part.text

def get_Summary(texts: list)->str:
    if len(texts)>1:
        prompt = "A continuación te voy a dar unos textos numerados empezando por el 0. Quiero un resumen en detalle por separado de cada uno de ellos de máximo unas 6 líneas"
        for index, text in enumerate(texts):
            prompt+= f'\n {index}:  {text}'
        return get_chat_response(chat, prompt)
    else:
        return ''