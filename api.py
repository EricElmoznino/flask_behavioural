from flask import Flask, request, send_file, abort
from flask_cors import CORS
import json
from experiments import *

experiment = Greene2009()

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return send_file(experiment.web_path)


@app.route('/get_trial', methods=['GET'])
def get_trial():
    trial = experiment.generate_trial()
    return trial


@app.route('/post_responses', methods=['POST'])
def post_responses():
    responses = request.json
    experiment.trial_done(responses)
    return '', 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=False)
