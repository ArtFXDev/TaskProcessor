from __future__ import annotations

import taskprocessor.core.engine as eg
import taskprocessor.core as core


class Job(object):

    def __init__(self, engine: eg.Engine, tasks: list[core.Task]):
        self.engine = engine
        self.tasks: list[core.Task] = tasks

        self.engine.add_start_listener(self.on_execution_started)
        self.engine.add_progress_listener(self.on_execution_progress)
        self.engine.add_complete_listener(self.on_execution_completed)

    def __del__(self):
        self.engine.remove_start_listener(self.on_execution_started)
        self.engine.remove_progress_listener(self.on_execution_progress)
        self.engine.remove_complete_listener(self.on_execution_completed)

    def on_execution_started(self, entity_path: str, status: str):
        index = next((i for (i, t) in enumerate(self.tasks) if t.entity.path == entity_path))
        print("Executing {} of {}:".format(index + 1, len(self.tasks)))
        print(status)

    def on_execution_progress(self, entity_path: str, progress: float, status: str):
        # index = next((i for (i, t) in enumerate(self.tasks) if t.entity.path == entity_path))
        # print("Progress {} of {}: {}".format(index + 1, len(self.tasks), progress))
        print(status, end="")

    def on_execution_completed(self, entity_path: str, success: bool, status: str):
        index = next((i for (i, t) in enumerate(self.tasks) if t.entity.path == entity_path))
        print("Completed {} of {}: {}".format(index + 1, len(self.tasks), success))
        print(status)

    def start(self):
        for t in self.tasks:
            print("\nFinal Code for Entity: {}:".format(t.entity.label))
            code = t.get_code()
            print(code)
            self.engine.execute(t.entity.path, code)
