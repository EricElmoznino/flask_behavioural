from flask import Flask, request, send_file
from flask_cors import CORS
from experiments import *

experiment = Greene2009()

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return send_file(experiment.web_path)


@app.route('/get_trials', methods=['GET'])
def get_trials():
    trials = experiment.generate_trials()
    return trials


@app.route('/post_responses', methods=['POST'])
def post_responses():
    responses = request.json
    experiment.trial_done(responses)
    return {}


if __name__ == "__main__":
    app.run()
