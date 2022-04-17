from __future__ import annotations

import taskprocessor.utils.json_utils as json_utils


class EngineData(object):

    def __init__(self, name: str = "python", extensions: list[str] = None, exec_path: str = "python.exe"):
        self.name: str = name
        self.extensions: list[str] = extensions
        self.exec_path: str = exec_path

    # Covert current ActionData object from dict to string
    def __str__(self):
        data = self.__dict__
        return json_utils.dict_to_json(data)

    # Get json string from current ActionData object
    def to_json(self) -> str:
        return self.__str__()

    # Get a ActionData object from json string
    @staticmethod
    def from_json(json_data) -> EngineData:
        # TODO: Throw exceptions on fail
        json_dict = json_utils.json_to_dict(json_data)
        engine_data = EngineData(json_dict['name'], json_dict['extensions'], json_dict['exec_path'])
        return engine_data
