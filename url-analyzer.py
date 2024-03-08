#NLP libraries
import spacy
from spacy.matcher import Matcher
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

from collections import defaultdict


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
#Almacenamos las frases una vez lematizadas y si contienen o no la frase formato
# Formato : [0/1,frase]
# 0 Indica que no contiene
# 1 Indica que si contiene
sentences = []
#Procesamiento de normalización y detección de entidades
for doc in docs:
    for sent in doc.sents:
        sentence = []
        #Indica si una frase contiene keyword, se pone a False cuando contiene, true no contiene
        first = True
        for token in sent:
            #Aparece keyword por lo tanto aumentar contador
            if token.text.lower() == word and first:
                first = False
                phrasesKeyword['YES'] +=1
            #if not token.is_stop:
            sentence.append(token.lemma_)
        contains = 1
        #Si no aparece keyword aumentar en 1 contador no
        if first:
            contains = 0
            phrasesKeyword['NO'] +=1
        sentences.append([contains," ".join(sentence)])
    for ent in doc.ents:
        if ent.label_ not in entitiesCount:
            entitiesCount[ent.label_] = 1
        else:
            entitiesCount[ent.label_] += 1

print(entitiesCount)

#Asignamos a cada frase un valor entre [0,1] y seguimos manteniendo si contiene o no keyword
sentiment_results = []
for element in sentences:
    sentiment_results.append([element[0],sentiment_spanish.sentiment(element[1])])
#print(sentiment_results)

sent_class_arr = []
labToVal = {}
sentimentKeyword = {
    0: defaultdict(int),
    1: defaultdict(int)
}
#Asignar según cada valor un count
for res in sentiment_results:
    if res[1] > 0.5:
        sent = 'POS'
    elif res[1] > 0.001:
        sent = 'NEU'
    else:
        sent = 'NEG'
    sent_class_arr.append(sent[1])
    if sent not in labToVal:
        labToVal[sent] = 1
    else:
        labToVal[sent] += 1
    if res[0] == 0:
        sentimentKeyword[0][sent] +=1
    else:
        sentimentKeyword[1][sent] +=1
    
if len(failedUrls)>0:
    print(len(failedUrls) , " have failed: ")
    i=1
    for url in failedUrls:
        print(i,". ",url)
        i += 1

print(labToVal)
print(phrasesKeyword)
#No contiene keyword
print(sentimentKeyword[0])
#Contiene Keyword
print(sentimentKeyword[1])

#Crear y mostrar gráficas
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10, 7))

colors = ['blue', 'green', 'skyblue', 'yellow']

df_bar = pd.DataFrame({'Sentimiento':list(labToVal.keys()), 'Cantidad': list(labToVal.values())})
df_bar.plot.bar(x='Sentimiento',y='Cantidad', rot = 0,ax=axes[0,0], color=colors)
axes[0,0].set_title('Phrases Distribution')

df_pie = pd.DataFrame({'Name':list(labToVal.keys()), 'val': list(labToVal.values())})
df_pie.plot(kind='pie', y='val', autopct='%1.0f%%', labels=df_pie['Name'],ax=axes[0,1])
axes[0,1].set_title('Percentage of total phrases')

df_Entities = pd.DataFrame({'Tipos':list(entitiesCount.keys()), 'Cantidad': list(entitiesCount.values())})
df_Entities.plot.bar(x='Tipos',y='Cantidad', rot = 0,ax=axes[0,2], color=colors)
axes[0,2].set_title('Entities Spotted')

df_ContainsKeyowrd = pd.DataFrame({'Contiene':list(phrasesKeyword.keys()), 'Cantidad': list(phrasesKeyword.values())})
df_ContainsKeyowrd.plot.barh(x='Contiene',y='Cantidad', rot=0,ax=axes[1,0], color= 'lightblue')
axes[1,0].set_title('Phrase contains keyword?')

df_PhrasesWithKeyword = pd.DataFrame({'Sentimiento':list(sentimentKeyword[1].keys()), 'Cantidad': list(sentimentKeyword[1].values())})
df_PhrasesWithKeyword.plot.bar(x='Sentimiento',y='Cantidad', rot = 0,ax=axes[1,1], color=colors)
axes[1,1].set_title('Phrases with keyword')

df_PhrasesWithoutKeyword = pd.DataFrame({'Sentimiento':list(sentimentKeyword[0].keys()), 'Cantidad': list(sentimentKeyword[0].values())})
df_PhrasesWithoutKeyword.plot.bar(x='Sentimiento',y='Cantidad', rot = 0,ax=axes[1,2], color=colors)
axes[1,2].set_title('Phrases without keyword')


plt.tight_layout()
plt.show()

