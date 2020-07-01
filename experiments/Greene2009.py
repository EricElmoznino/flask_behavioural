import os
import random
random.seed(27)
import json
from .BaseExperiment import BaseExperiment


class Greene2009(BaseExperiment):

    def __init__(self, name):
        super().__init__(name='greene2009_{}'.format(name),
                         template='greene2009.html', template_data=template_data[name])

        self.data_dir = 'static/greene2009/' + name
        with open(os.path.join(self.data_dir, 'trials.json'), 'r') as f:
            self.data = json.loads(f.read())

        conditions = os.listdir(self.data_dir)
        self.rois = [c for c in conditions if c not in ['catch', 'examples', 'trials.json']]

    def generate_trials(self):
        # Randomize positive/negative pairs of the test set
        random.shuffle(self.data['test']['positives'])

        # Make trials
        trials = {}
        image_paths = []

        for phase in ['train', 'test']:
            phase_trials = []
            for pos, neg in zip(self.data[phase]['positives'], self.data[phase]['negatives']):
                for roi in self.rois:
                    trial = self.create_trial(pos, neg, roi)
                    phase_trials.append(trial)
                    image_paths += trial['images']
            trials[phase] = phase_trials

        # Add in catch trials to the testing phase
        catch_trials = []
        for pos, neg in zip(self.data['catch']['positives'], self.data['catch']['negatives']):
            trial = self.create_trial(pos, neg, 'catch')
            catch_trials.append(trial)
            image_paths += trial['images']
        trials['test'] = trials['test'] + catch_trials

        # Randomize order in which trials are being shown
        random.shuffle(trials['train'])
        random.shuffle(trials['test'])

        return {'trials': trials, 'imagePaths': image_paths}

    def create_trial(self, pos, neg, condition):
            images = [os.path.join(self.data_dir, condition, pos),
                      os.path.join(self.data_dir, condition, neg)]
            option_order = ['pos', 'neg']

            # Randomize the left/right order of the positive/negative pair
            if random.random() < 0.5:
                images = images[::-1]
                option_order = option_order[::-1]

            trial = {
                'images': images,
                'optionOrder': option_order,
                'condition': condition
            }

            return trial


template_data = {
    'concealment': {
        'attribute': 'concealment', 'goal': 'has more concealment',
        'negLabel': 'Low concealment', 'posLabel': 'High concealment',
        'negDescription': 'If standing in the scene, one would be easily seen.',
        'posDescription': 'The scene contains many accessible hiding spots, and there may be hidden objects in the scene.'
    }, 'depth': {
        'attribute': 'depth', 'goal': 'has more depth',
        'negLabel': 'Low depth', 'posLabel': 'High depth',
        'negDescription': 'The scene takes up less than a few feet of space.',
        'posDescription': 'The scene takes up miles of depth.'
    },

}
