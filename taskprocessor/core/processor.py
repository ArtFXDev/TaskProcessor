from __future__ import annotations
from typing import Callable

import taskprocessor.core as core
import taskprocessor.core.engine as eg


class Processor(object):

    def __init__(self, engine: eg.Engine):
        self.engine: eg.Engine = engine
        self.current_job: core.Job | None = None

        self._start_listeners = []
        self._progress_listeners = []
        self._error_listeners = []
        self._complete_listeners = []

    def add_on_start_listener(self, callback: Callable[[str], None]):
        self._start_listeners.append(callback)

    def remove_on_start_listener(self, callback: Callable[[str], None]):
        self._start_listeners.remove(callback)

    def add_on_progress_listener(self, callback: Callable[[str, str, float, float, str], None]):
        self._progress_listeners.append(callback)

    def remove_on_progress_listener(self, callback: Callable[[str, str, float, float, str], None]):
        self._progress_listeners.remove(callback)

    def add_on_error_listener(self, callback: Callable[[str], None]):
        self._error_listeners.append(callback)

    def remove_on_error_listener(self, callback: Callable[[str], None]):
        self._error_listeners.remove(callback)

    def add_on_completed_listener(self, callback: Callable[[bool, str], None]):
        self._complete_listeners.append(callback)

    def remove_on_completed_listener(self, callback: Callable[[bool, str], None]):
        self._complete_listeners.remove(callback)

    def on_job_started(self, job: core.Job, status: str):
        for listener in self._start_listeners:
            listener(status)

    def on_job_error(self, job: core.Job, status: str):
        for listener in self._error_listeners:
            listener(status)

    def on_job_progress(self, job: core.Job, status: str):
        for listener in self._progress_listeners:
            listener(job.current_task.label, job.current_action.id, job.total_progress, job.current_task_progress,
                     status)

    def on_job_completed(self, job: core.Job, is_success: bool, status: str):
        for listener in self._complete_listeners:
            listener(is_success, status)

        self.current_job.remove_start_listener(self.on_job_started)
        self.current_job.remove_progress_listener(self.on_job_progress)
        self.current_job.remove_error_listener(self.on_job_error)
        self.current_job.remove_complete_listener(self.on_job_completed)
        self.current_job = None

    def create_job(self,
                   entities: list[core.Entity],
                   actions: list[core.ActionRuntime]):
        tasks = []
        for e in entities:
            task = core.Task(e, actions, e.label)
            tasks.append(task)
        self.current_job = core.Job(self.engine, tasks)

        self.current_job.add_start_listener(self.on_job_started)
        self.current_job.add_progress_listener(self.on_job_progress)
        self.current_job.add_error_listener(self.on_job_error)
        self.current_job.add_complete_listener(self.on_job_completed)

    def start(self):
        self.current_job.start()

    def pause(self):
        pass

    def stop(self):
        pass
