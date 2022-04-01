from __future__ import annotations
from typing import Callable

import taskprocessor.core.engine as eg
import taskprocessor.core as core


class Job(object):

    def __init__(self, engine: eg.Engine, tasks: list[core.Task]):
        self.engine = engine
        self.tasks: list[core.Task] = tasks

        self._start_listeners = []
        self._progress_listeners = []
        self._error_listeners = []
        self._complete_listeners = []

        self._is_start_listener_added = False
        self._is_progress_listener_added = False
        self._is_error_listener_added = False
        self._is_complete_listener_added = False

        self._curr_task_index: int = 0
        self._curr_task: core.Task | None = None
        self._curr_task_progress: float = 0.0
        self._curr_action: core.ActionRuntime | None = None
        self._total_progress: float = 0.0

    @property
    def current_task_index(self):
        return self._curr_task_index

    @property
    def current_task(self):
        return self._curr_task

    @property
    def current_task_progress(self):
        return self._curr_task_progress

    @property
    def current_action(self):
        return self._curr_action

    @property
    def total_progress(self):
        return self._total_progress

    def add_start_listener(self, callback: Callable[[Job, str], None]):
        # If not subscribed, subscribe to engine start
        if not self._is_start_listener_added:
            self.engine.add_start_listener(self.on_engine_started)
            self._is_start_listener_added = True

        self._start_listeners.append(callback)

    def remove_start_listener(self, callback: Callable[[Job, str], None]):
        # If subscribed, unsubscribe to engine start
        if self._is_start_listener_added:
            self.engine.remove_start_listener(self.on_engine_started)
            self._is_start_listener_added = False

        self._start_listeners.remove(callback)

    def add_progress_listener(self, callback: Callable[[Job, str], None]):
        # If not subscribed, subscribe to engine progress
        if not self._is_progress_listener_added:
            self.engine.add_progress_listener(self.on_engine_progress)
            self._is_progress_listener_added = True

        self._progress_listeners.append(callback)

    def remove_progress_listener(self, callback: Callable[[Job, str], None]):
        # If subscribed, unsubscribe to engine progress
        if self._is_progress_listener_added:
            self.engine.remove_progress_listener(self.on_engine_progress)
            self._is_progress_listener_added = False

        self._progress_listeners.remove(callback)

    def add_error_listener(self, callback: Callable[[Job, str], None]):
        self._error_listeners.append(callback)

    def remove_error_listener(self, callback: Callable[[Job, str], None]):
        self._error_listeners.remove(callback)

    def add_complete_listener(self, callback: Callable[[Job, bool, str], None]):
        # If not subscribed, subscribe to engine complete
        if not self._is_complete_listener_added:
            self.engine.add_complete_listener(self.on_engine_completed)
            self._is_complete_listener_added = False

        self._complete_listeners.append(callback)

    def remove_complete_listener(self, callback: Callable[[Job, bool, str], None]):
        # If subscribed, unsubscribe to engine complete
        if self._is_complete_listener_added:
            self.engine.remove_complete_listener(self.on_engine_completed)
            self._is_complete_listener_added = False

        self._complete_listeners.remove(callback)

    def on_engine_started(self, entity_path: str, status: str):
        self._curr_task = next((t for t in self.tasks if t.entity.path == entity_path), None)
        self._curr_task_index = self.tasks.index(self._curr_task)
        self._curr_action = self._curr_task.actions[0]
        self._curr_task_progress = 0.0

        # For first task send Job start event
        if self._curr_task_index == 0:
            for listener in self._start_listeners:
                listener(self, status)

    def on_engine_progress(self, entity_path: str, action_id: str, progress: float, status: str, is_err: bool):
        if not is_err:
            if str(self._curr_action.id) is not action_id:
                self._curr_action = next((a for a in self._curr_task.actions if str(a.id) == action_id), None)

            self._curr_task_progress = progress
            self._total_progress = (self._curr_task_index + progress) / len(self.tasks)

            for listener in self._progress_listeners:
                listener(self, status)
        else:
            for listener in self._error_listeners:
                listener(self, status)

    def on_engine_completed(self, entity_path: str, success: bool, status: str):
        # For last task send Job end event
        if self._curr_task_index == len(self.tasks) - 1:
            for listener in self._complete_listeners:
                listener(self, success, status)
        else:
            self._curr_task = self.tasks[self._curr_task_index + 1]
            self._curr_task_index += 1
            self._curr_action = self._curr_task.actions[0]
            self._curr_task_progress = 0.0

    def start(self):
        for t in self.tasks:
            # print("\nFinal Code for Entity: {}:".format(t.entity.label))
            code = t.get_code()
            # print(code)
            self.engine.execute(t.entity.path, code)
