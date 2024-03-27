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

from collections import defaultdict




from vertexAPI import CustomThread

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
cookies = {
}

def analyzeUrls(urls, keyword = None, singleUrl = False) -> dict:
    texts = []
    failedUrls = []
    fullArticles = []
    promptTexts = []

    for url in urls:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            print(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            with open('Data.txt', 'a', encoding='utf-8') as out_f:
                for paragraph in soup.find_all(['p','h1','h2','h3']):
                    texts.append(paragraph.text)
                    fullArticles.append(paragraph.text)
                    out_f.write(paragraph.text)
                    out_f.write('\n\n')
        else:
            failedUrls.append(url)
            print(response)
            print(f"Failed to retrieve content from {url}")
        promptTexts.append(" ".join(fullArticles))
        fullArticles = []

    if not singleUrl:
        thread_gemini_text = CustomThread(promptTexts)
        thread_gemini_text.start()
        

    #Phrases with KeyWord
    phrasesKeyword = {
        'YES': 0,
        'NO': 0
    }
    #Almacenar por cada tipo de entidad su conteo
    entitiesCount={}
    #Procesamos los textos de las webs con spacy
    docs = [doc for doc in nlp.pipe(texts)]
    #Almacenamos las frases una vez lematizadas y si contienen o no el keyword
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
                if token.text.lower() == keyword.lower() and first:
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
    #Guarda resultado global
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
        
    #Global response
    print(labToVal)
    print(phrasesKeyword)
    #No contiene keyword
    print(sentimentKeyword[0])
    #Contiene Keyword
    print(sentimentKeyword[1])

    #Sentiment repeated the most
    overallSentCoun = 0
    overallSent = None
    for key, value in labToVal.items():
        if value >= overallSentCoun:
            overallSentCoun = value
            overallSent = key

    if not singleUrl:
        thread_gemini_text.join()
        print(thread_gemini_text.value)
    return {
        'overallSent': overallSent,
        'globalResults': labToVal, 
        'phraseContainsKeyword': {
            'count':phrasesKeyword,
            'no': sentimentKeyword[0],
            'yes': sentimentKeyword[1]
        },
        'entitiesSpotted': entitiesCount,
        'failedUrls': failedUrls,
        'summary': thread_gemini_text.value if not singleUrl else None,
        }
