from __future__ import annotations

import subprocess, os, sys, datetime, json
from pathlib import Path

from src.experiment import Experiment


class Task:
    def __init__(self, id, experiment: Experiment, settings):
        self.id = id
        self.experiment = experiment
        self.settings = settings
        self._file_name = str(id)

    @property
    def log_output_path(self):
        return os.path.join(self.settings.output, self.experiment.name, 'logs', self._file_name + '.log')

    @property
    def measurements_output_path(self):
        return os.path.join(self.settings.output, self.experiment.name, 'measurements', self._file_name + '.csv')

    @property
    def info_output_path(self):
        return os.path.join(self.settings.output, self.experiment.name, 'info', self._file_name + '.json')

    def run(self):
        EnergiBridge(self.settings).run(self)

class EnergiBridge:
    def __init__(self, settings) -> None:
        self.settings = settings
        pass

    def cmd(self, task: Task):
        program_path = '\"' + os.path.join(os.path.dirname(__file__), "..", "energibridge", "energibridge")
        if sys.platform == "win32":
            program_path += ".exe"
        program_path += '\"'
        return [program_path, "-i", str(self.settings.interval), "--max-execution", str(task.experiment.max_execution),
                "-o", f"\"{task.measurements_output_path}\"", "--command-output", f"\"{task.log_output_path}\""]

    def run(self, task: Task):
        start = datetime.datetime.now()

        os.makedirs(os.path.dirname(task.measurements_output_path), exist_ok=True)
        os.makedirs(os.path.dirname(task.log_output_path), exist_ok=True)
        os.makedirs(os.path.dirname(task.info_output_path), exist_ok=True)
        o = {
            "startingTime": start.isoformat(),
            "energiBridgeCmd": " ".join(self.cmd(task)),
            "taskCmd": task.experiment.command,
        }

        file = Path(task.log_output_path).relative_to(os.getcwd()).as_posix()
        os.environ["FFREPORT"] = f'file={file}:level=32'
        os.environ["RUST_BACKTRACE"] = "full"
        print(f"[TASK {task.experiment.name} - {task.id}] started at {start}", end=' ')
        try:
            process = subprocess.Popen(" ".join(self.cmd(task) + ['--', task.experiment.command]), shell=True)
            process.wait()
        finally:
            print(f"DONE in {datetime.datetime.now() - start}")
            o["endingTime"] = datetime.datetime.now().isoformat()
            with open(task.info_output_path, "w") as f:
                json.dump(o, f, indent=4)
