from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['POST'])
@cross_origin()
def hello_world():
    data = request.get_json()
    print(data['urls'])
    return {
        "status": 200,
        "name": "aaaa"
    }