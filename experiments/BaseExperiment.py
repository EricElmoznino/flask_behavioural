import pandas as pd


class BaseExperiment:

    def __init__(self, name, web_path):
        self.name = name
        self.web_path = web_path

    def trial_done(self, responses):
        pass

    def generate_trial(self):
        raise NotImplementedError()
