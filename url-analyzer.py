#NLP libraries
import spacy
from sentiment_analysis_spanish import sentiment_analysis

nlp = spacy.load('es_core_news_sm')
sentiment_spanish = sentiment_analysis.SentimentAnalysisSpanish()

import requests
#Web scrapping library
from bs4 import BeautifulSoup
#Libraries for stadistics and graphs representations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
cookies = {
}
urls = [
    "https://www.xataka.com/analisis/iphone-15-iphone-15-plus-analisis-caracteristicas-precio",
    "https://elpais.com/tecnologia/tu-tecnologia/2023-09-27/el-iphone-15-a-prueba-lo-mejor-y-lo-peor-del-movil-de-gama-alta-mas-asequible-de-apple.html"
]
word = "apple"
texts = []
failedUrls = []
for url in urls:
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        with open('Data.txt', 'a', encoding='utf-8') as out_f:
            for paragraph in soup.find_all(['p','h1','h2','h3']):
                texts.append(paragraph.text)
                out_f.write(paragraph.text)
                out_f.write('\n\n')
    else:
        failedUrls.append(url)
        print(response)
        print(f"Failed to retrieve content from {url}")



#Phrases with KeyWord
phrasesKeyword = {
    'YES': 0,
    'NO': 0
}
#Almacenar por cada tipo de entidad su conteo
entitiesCount={}
#Procesamos los textos de las webs con spacy
docs = [doc for doc in nlp.pipe(texts)]
#Almacenamos las frases una vez lematizadas
sentences = []
#Procesamiento de normalización y detección de entidades
for doc in docs:
    for sent in doc.sents:
        sentence = []
        first = True
        for token in sent:
            #Aparece keyword por lo tanto aumentar contador
            if token.text.lower() == word and first:
                first = False
                phrasesKeyword['YES'] +=1
            #if not token.is_stop:
            sentence.append(token.lemma_)
        sentences.append(" ".join(sentence))
        #Si no aparece keyword aumentar en 1 contador no
        if first:
            phrasesKeyword['NO'] +=1
    for ent in doc.ents:
        if ent.label_ not in entitiesCount:
            entitiesCount[ent.label_] = 1
        else:
            entitiesCount[ent.label_] += 1

print(entitiesCount)

#Asignamos a cada frase un valor entre [0,1] 
sentiment_results = [sentiment_spanish.sentiment(text) for text in sentences]
#print(sentiment_results)

sent_class_arr = []
labToVal = {}
#Asignar según cada valor un count
for res in sentiment_results:
    if res > 0.7:
        sent = 'POS'
    elif res > 0.001:
        sent = 'NEU'
    else:
        sent = 'NEG'
    sent_class_arr.append(sent)
    if sent not in labToVal:
        labToVal[sent] = 1
    else:
        labToVal[sent] += 1

if len(failedUrls)>0:
    print(len(failedUrls) , " have failed: ")
    i=1
    for url in failedUrls:
        print(i,". ",url)
        i += 1

print(labToVal)
print(phrasesKeyword)

#Crear y mostrar gráficas
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

df_bar = pd.DataFrame({'lab':list(labToVal.keys()), 'val': list(labToVal.values())})
df_bar.plot.bar(x='lab',y='val', rot = 0,ax=axes[0])
axes[0].set_title('Bar Chart')

df_pie = pd.DataFrame({'Name':list(labToVal.keys()), 'val': list(labToVal.values())})
df_pie.plot(kind='pie', y='val', autopct='%1.0f%%', labels=df_pie['Name'],ax=axes[1])
axes[1].set_title('Pie Chart')

plt.tight_layout()
plt.show()

