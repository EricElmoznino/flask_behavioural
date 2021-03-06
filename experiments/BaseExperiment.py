import os
import json
from datetime import datetime


class BaseExperiment:

    def __init__(self, name, template, template_data):
        self.name = name
        self.template = template
        self.template_data = template_data

        self.save_dir = os.path.join('results', name)
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

    def trial_done(self, responses):
        time = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        with open(os.path.join(self.save_dir, time + '.json'), 'w') as f:
            f.write(json.dumps(responses))

    def generate_trials(self):
        raise NotImplementedError()
