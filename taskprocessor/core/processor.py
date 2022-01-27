from __future__ import annotations

import  taskprocessor.core as core
import taskprocessor.core.engine as eg

class Processor(object):

    def __init__(self, engine: eg.Engine):
        self.engine = engine
        self.current_job: [core.Job] = None

    def create_job(self, entities, actions):
        tasks = []
        for e in entities:
            task = core.Task(e)
            task.add_actions(actions)
            tasks.append(task)
        self.current_job = core.Job(tasks)

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    # Overrides the call operator [ () ] and process the given tasks
    def __call__(self, *args, **kwargs):
        # TODO: Add job execution.
        self.job.start()
        pass
