from __future__ import annotations

import io
import subprocess
from typing import Callable

import taskprocessor.core.engine as engine
import taskprocessor.utils.path_utils as path_utils
import taskprocessor.utils.json_utils as json_utils


class Engine(object):

    def __init__(self, engine_config_path: str):
        self.engine_data: [engine.EngineData] = [engine.EngineData()]
        self.set_engine_data(engine_config_path)
        self.current_engine: [engine.EngineData] = self.engine_data[0]

        self.__progress_listeners = []
        self.__start_listeners = []
        self.__complete_listeners = []

    def set_engine_data(self, engine_config_path: str):
        config_file_contents = path_utils.read_file(engine_config_path)
        config_dict = json_utils.json_to_dict(config_file_contents)
        self.engine_data = []
        for d in config_dict['data']:
            self.engine_data.append(engine.EngineData.from_json(json_utils.dict_to_json(d)))

    def is_engine_supported(self, entity_extensions: [str]) -> bool:
        for ext in entity_extensions:
            for ed in self.engine_data:
                if ext in ed.extensions:
                    return True
        return False

    def get_engine_data_by_extension(self, extension) -> engine.EngineData | None:
        return next((e for e in self.engine_data if extension in e.extensions), None)

    # TODO: Set current engine by the current selection of entities
    def set_current_engine(self, name) -> bool:
        eg = next((e for e in self.engine_data if e.name.lower() == name.lower()), None)
        if eg is None:
            return False
        self.current_engine = eg
        return True

    def add_progress_listener(self, callback: Callable[[str, float, str], None]):
        self.__progress_listeners.append(callback)

    def remove_progress_listener(self, callback: Callable[[str, float, str], None]):
        self.__progress_listeners.remove(callback)

    def add_start_listener(self, callback: Callable[[str, str], None]):
        self.__start_listeners.append(callback)

    def remove_start_listener(self, callback: Callable[[str, str], None]):
        self.__start_listeners.remove(callback)

    def add_complete_listener(self, callback: Callable[[str, bool, str], None]):
        self.__complete_listeners.append(callback)

    def remove_complete_listener(self, callback: Callable[[str, bool, str], None]):
        self.__complete_listeners.remove(callback)

    def __execute(self, entity_path: str, exec_file: io.TextIOWrapper):
        is_success = True

        args = [self.current_engine.exec_path, exec_file.name]
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as subp:
            stdout = subp.stdout.read().decode()
            stderr = subp.stderr.read().decode()

            if len(stderr) > 0:
                is_success = False

            # TODO: Add better status text handling
            status = """
            Execution Status: IN-PROGRESS
            Execution Output: {0}
            Execution Error: {1}
            """.format(stdout, stderr, 1.0)

            for p in self.__progress_listeners:
                p(entity_path, 1.0, status)

        is_success = is_success and path_utils.delete_temp_file(exec_file)

        # TODO: Add better status text handling
        exec_complete_status = """
        Execution Status: COMPLETED
        Execution Engine: {0}
        Execution Success: {1}
        Execution Code File: {2}
        """.format(self.current_engine.name.upper(), is_success, exec_file.name)

        for c in self.__complete_listeners:
            c(entity_path, True, exec_complete_status)

    def execute(self, entity_path: str, exec_code: str):
        temp_exec_file = path_utils.get_temp_file(exec_code, "tp_{0}_".format(self.current_engine.name), "py")

        # TODO: Add better status text handling
        exec_start_status = """
        Execution Status: START
        Execution Engine: {0}
        Execution Code File: {1}
        """.format(self.current_engine.name.upper(), temp_exec_file.name)

        for s in self.__start_listeners:
            s(entity_path, exec_start_status)

        self.__execute(entity_path, temp_exec_file)
