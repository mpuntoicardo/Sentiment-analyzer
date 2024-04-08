from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin

from url_analyzer import analyzeUrls

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