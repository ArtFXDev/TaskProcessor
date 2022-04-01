from __future__ import annotations

import io
import subprocess
from typing import Callable
from threading import Thread
from queue import Queue, Empty

import taskprocessor.core
from taskprocessor.core import ACTION_EXECUTION_STARTED_KEYWORD, ACTION_EXECUTION_COMPLETED_KEYWORD
from taskprocessor.core.engine import EngineData
import taskprocessor.utils.path_utils as path_utils
import taskprocessor.utils.json_utils as json_utils


class Engine(object):

    def __init__(self, engine_config_path: str):
        self.engine_data: [EngineData] = [EngineData()]
        self.set_engine_data(engine_config_path)
        self.current_engine: [EngineData] = self.engine_data[0]

        self._progress_listeners = []
        self._start_listeners = []
        self._complete_listeners = []

    def set_engine_data(self, engine_config_path: str):
        config_file_contents = path_utils.read_file(engine_config_path)
        config_dict = json_utils.json_to_dict(config_file_contents)
        self.engine_data = []
        for d in config_dict['data']:
            self.engine_data.append(EngineData.from_json(json_utils.dict_to_json(d)))

    def is_engine_supported(self, entity_extensions: [str]) -> bool:
        for ext in entity_extensions:
            for ed in self.engine_data:
                if ext in ed.extensions:
                    return True
        return False

    def get_engine_data_by_extension(self, extension) -> EngineData | None:
        return next((e for e in self.engine_data if extension in e.extensions), None)

    # TODO: Set current engine by the current selection of entities
    def set_current_engine(self, name) -> bool:
        eg = next((e for e in self.engine_data if e.name.lower() == name.lower()), None)
        if eg is None:
            return False
        self.current_engine = eg
        return True

    def add_progress_listener(self, callback: Callable[[str, str, float, str, bool], None]):
        self._progress_listeners.append(callback)

    def remove_progress_listener(self, callback: Callable[[str, str, float, str, bool], None]):
        self._progress_listeners.remove(callback)

    def add_start_listener(self, callback: Callable[[str, str], None]):
        self._start_listeners.append(callback)

    def remove_start_listener(self, callback: Callable[[str, str], None]):
        self._start_listeners.remove(callback)

    def add_complete_listener(self, callback: Callable[[str, bool, str], None]):
        self._complete_listeners.append(callback)

    def remove_complete_listener(self, callback: Callable[[str, bool, str], None]):
        self._complete_listeners.remove(callback)

    def __enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def __execute(self, entity_path: str, exec_file: io.TextIOWrapper):
        is_success = True

        # Sanitize executable file path
        exec_path = path_utils.get_absolute_path(exec_file.name)

        args = [self.current_engine.exec_path, exec_path]

        curr_progress = 0.0
        curr_action = ""

        subp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_thread = Thread(target=self.__enqueue_output, args=(subp.stdout, stdout_queue))
        # stdout_thread.daemon = True
        stderr_queue = Queue()
        stderr_thread = Thread(target=self.__enqueue_output, args=(subp.stderr, stderr_queue))
        # stderr_thread.daemon = True

        stdout_thread.start()
        stderr_thread.start()

        while subp.poll() is None:
            try:
                stdout_line = stdout_queue.get_nowait()
            except Empty:
                pass
            else:
                data = stdout_line.decode("utf-8")
                # TODO: Find a better way to deal with action data
                action_id = curr_action
                progress = curr_progress
                if ACTION_EXECUTION_STARTED_KEYWORD in data:
                    action_id = data.split('|')[1].strip()
                    data = ""
                elif ACTION_EXECUTION_COMPLETED_KEYWORD in data:
                    progress = float(data.split('|')[1].strip())
                    data = ""

                if action_id is not curr_action or progress is not curr_progress:
                    curr_action = action_id
                    curr_progress = progress
                    for p in self._progress_listeners:
                        p(entity_path, curr_action, curr_progress, data, False)

            try:
                stderr_line = stderr_queue.get_nowait()
            except Empty:
                pass
            else:
                for p in self._progress_listeners:
                    p(entity_path, curr_action, curr_progress, stderr_line.decode("utf-8"), True)

        stdout_thread.join()
        stderr_thread.join()

        is_tmp_deleted = path_utils.delete_temp_file(exec_file)
        is_success = is_success and is_tmp_deleted

        # TODO: Add better status text handling
        exec_complete_status = """
        Execution Status: COMPLETED
        Execution Engine: {0}
        Execution Success: {1}
        Execution Code File: {2}
        """.format(self.current_engine.name.upper(), is_success, exec_file.name)

        for c in self._complete_listeners:
            c(entity_path, True, exec_complete_status)

    def execute(self, entity_path: str, exec_code: str):
        temp_exec_file = path_utils.get_temp_file(exec_code, "tp_{0}_".format(self.current_engine.name), "py")

        # TODO: Add better status text handling
        exec_start_status = """
        Execution Status: START
        Execution Engine: {0}
        Execution Code File: {1}
        """.format(self.current_engine.name.upper(), temp_exec_file.name)

        for s in self._start_listeners:
            s(entity_path, exec_start_status)

        self.__execute(entity_path, temp_exec_file)
