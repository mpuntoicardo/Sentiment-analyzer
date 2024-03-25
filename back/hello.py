from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin

from url_analyzer import analyzeUrls

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['POST'])
@cross_origin()
def hello_world():
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


    return jsonify(results), 200