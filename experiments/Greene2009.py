import os
import random
random.seed(27)
from .BaseExperiment import BaseExperiment

name = 'concealment'
images_dir = 'assets/greene2009_concealment'
web_path = 'static/greene2009/concealment.html'


class Greene2009(BaseExperiment):

    def __init__(self):
        super().__init__('greene2009_{}'.format(name), web_path)

    def generate_trial(self):
        return {'test': True}
