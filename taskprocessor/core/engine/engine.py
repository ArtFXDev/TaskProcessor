from __future__ import annotations

import io
import subprocess
from typing import Callable

import taskprocessor.core.engine as engine
import taskprocessor.utils.path_utils as path_utils
import taskprocessor.utils.json_utils as json_utils


class Engine(object):

    def __init__(self, engine_config_path: str):
        self.engine_data: [engine.EngineData] = []
        self.set_engine_data(engine_config_path)
        self.current_engine = self.engine_data[0]

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

    def set_current_engine(self, name) -> bool:
        eg = next((e for e in self.engine_data if e.name.lower() == name.lower()), None)
        if eg is None:
            return False
        self.current_engine = eg

    def add_progress_listener(self, callback: Callable[[str, float], None]):
        self.__progress_listeners.append(callback)

    def remove_progress_listener(self, callback: Callable[[str, float], None]):
        self.__progress_listeners.remove(callback)

    def add_start_listener(self, callback: Callable[[str], None]):
        self.__start_listeners.append(callback)

    def remove_start_listener(self, callback: Callable[[str], None]):
        self.__start_listeners.remove(callback)

    def add_complete_listener(self, callback: Callable[[bool, str], None]):
        self.__complete_listeners.append(callback)

    def remove_complete_listener(self, callback: Callable[[bool, str], None]):
        self.__complete_listeners.remove(callback)

    def __execute(self, entity_path: str, exec_file: io.TextIOWrapper):

        args = [self.executable, "-m", exec_file.name]
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as subp:
            for p in self.__progress_listeners:
                p(subp.stdout.read())

        # TODO: Add better status text handling
        exec_complete_status = """
        Execution Status: COMPLETED \n
        Execution Engine: {0} \n
        Execution Success: {1} \n
        Execution Code File: {2} \n
        """.format(self.name.upper(), True, exec_file.name)

        for c in self.__complete_listeners:
            c(True, exec_complete_status)

        path_utils.delete_temp_file(exec_file)

    def execute(self, entity_path: str, exec_code: str):
        temp_exec_file = path_utils.get_temp_file(exec_code, "tp_{0}".format(self.name), "py")

        # TODO: Add better status text handling
        exec_start_status = """
        Execution Status: START \n
        Execution Engine: {0} \n
        Execution Code File: {1} \n
        """.format(self.name.upper(), temp_exec_file.name)

        for s in self.__start_listeners:
            s(exec_start_status)

        self.__execute(entity_path, temp_exec_file)
