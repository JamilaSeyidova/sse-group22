import random
from time import sleep
from src.energiBridge import Task
from src.experiment import Experiment

def generate_tasks(experiments: [Experiment], settings):
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