import os
import random
from time import sleep
from energibridge.energiBridge import EnergiBridge
from energibridge.experiment import Experiment

class Task:
    def __init__(self, id, experiment: Experiment, settings):
        self.id = id
        self.experiment = experiment
        self.settings = settings

    @property
    def output_path(self):
        return os.path.join(self.settings.output, self.experiment.name, str(self.id))

    def run(self):
        EnergiBridge(self.settings).run(self)

def generate_tasks(experiments: [experiment], settings):
    tasks = []
    row = 0
    for experiment in experiments:
        for i in range(settings.iterations):
            tasks.append(Task(i + 1 + (row * settings.iterations), experiment, settings))
        row += 1
    tasks.sort(key = lambda x: random.random())
    warmup_experiment = Experiment("warmup")
    if settings.warmup > 0:
        return [Task(-1, warmup_experiment, settings)] + tasks
    else:
        return tasks

def run(experiments: [Experiment], settings):
    tasks = generate_tasks(experiments, settings)
    for task in tasks:
        task.run()
        sleep(settings.sleep)