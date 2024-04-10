from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin

from url_analyzer import analyzeUrls

from producer import publish

import requests, json

import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.dpvmmqw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['sentiment_analyzer']
collection = db['results']


@app.route("/urlsAnalyzer", methods=['POST'])
@cross_origin()
def urlsAnalysis():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    urls = data.get('urls')
    if not urls:
        return jsonify({"error": "No urls provided, bad request"}), 400
    keyword = data.get('keyword')
    if not keyword:
        keyword=''
    results = analyzeUrls(urls, keyword)
    result = collection.insert_one(results)
    if '_id' in results:
        results['_id'] = str(results['_id'])
    headers = request.headers['Authorization']
    #Comprobar que los headers enviados en la request son correctos
    if headers and len(headers.split())>1:
        isValidToken = requests.get('http://127.0.0.1:8000/test_token', headers={'Authorization': headers})
        #Validamos con el microservicio de django que sea un token valido
        if isValidToken.ok:
            #Pasamos de Json a dict
            contentDict = json.loads(isValidToken.content)
            publish({"result_id": results['_id'], "userId": contentDict['user']['id'], "urls": urls,"keyword": keyword, 'name':data.get('name') if data.get('name') else int(time.time()*1000) })
    return jsonify(results), 200

@app.route("/singleUrlAnalyzer", methods=['POST'])
@cross_origin()
def singleUrlAnalysis():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    url = data.get('url')
    if not url:
        return jsonify({"error": "No url provided, bad request"}), 400
    keyword = data.get('keyword')
    if not keyword:
        keyword=''
    results = analyzeUrls([url], keyword, True)
    return jsonify(results), 200