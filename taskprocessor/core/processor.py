from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.core.engine as eg


class Processor(object):

    def __init__(self, engine: eg.Engine):
        self.engine: eg.Engine = engine
        self.current_job: core.Job | None = None

    def on_job_started(self, job: core.Job, status: str):
        print("Job Started")

    def on_job_error(self, job: core.Job, status: str):
        print(f"Error: {status}")

    def on_job_progress(self, job: core.Job, status: str):
        print(
            f"Job Progress: {job.total_progress} | Task: {job.current_task.label} | Task Progress: {job.current_task_progress} | Action: {job.current_action.id}")

    def on_job_completed(self, job: core.Job, is_success: bool, status: str):
        print(f"Job Completed: {is_success}")

        self.current_job.remove_start_listener(self.on_job_started)
        self.current_job.remove_progress_listener(self.on_job_progress)
        # self.current_job.remove_error_listener(self.on_job_error)
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
        # self.current_job.add_error_listener(self.on_job_error)
        self.current_job.add_complete_listener(self.on_job_completed)

    def start(self):
        self.current_job.start()

    def pause(self):
        pass

    def stop(self):
        pass
