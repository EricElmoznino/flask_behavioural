from flask import Flask, request, render_template
from flask_cors import CORS
from experiments import *

experiment = Greene2009(name='depth')

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template(experiment.template, data=experiment.template_data)


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
