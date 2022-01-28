from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.core.engine as eg


class Processor(object):

    def __init__(self, engine: eg.Engine):
        self.engine: eg.Engine = engine
        self.current_job: core.Job | None = None

    def create_job(self, entities, actions):
        tasks = []
        for e in entities:
            task = core.Task(e)
            task.add_actions(actions)
            tasks.append(task)
        self.current_job = core.Job(self.engine, tasks)

    def start(self):
        self.current_job.start()

    def pause(self):
        pass

    def stop(self):
        pass
